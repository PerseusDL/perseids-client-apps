from fabric.api import *
from fabconf import user, hosts, path, available_hosts
from fabvenv import make_virtualenv
from datetime import datetime
import re

# Bad and hacky but only way to avoid __init__.py issues
execfile("app/configurations/modules.py")

# the user to use for the remote commands
env.user = user
# the servers where the commands are executed
env.hosts = hosts
env.remote_path = path
env.version = None
env.available_hosts = available_hosts

TIMESTAMP_FORMAT = "%Y%m%d%H%M%S"

def required_apt12():
    """ Install required app for ubuntu 12.04 """

    apt = [
        "apache2",
        "libxml2 libxml2-dev",
        "libxslt1-dev libxslt1.1",
        "git",
        "zlib1g-dev" # For XML etree
    ]
    python = [
        "python3.4",
        "python3.4-dev"
    ]

    # We will need to add some packages and do some specific things for Ubuntu 12.04
    sudo("apt-get install software-properties-common")
    sudo("apt-get install python-software-properties")
    sudo("add-apt-repository ppa:fkrull/deadsnakes")
    sudo("apt-get update")
    # Then we install
    sudo("apt-get install {0}".format(" ".join(apt + python)))
    # Then PIP
    run("wget https://pypi.python.org/packages/source/d/distribute/distribute-0.6.38.tar.gz")
    run("tar -xvf distribute-0.6.38.tar.gz")
    with cd("distribute-0.6.38"):
        sudo("python3.4 setup.py install")
        sudo("easy_install-3.4 pip")
    # Then venv
    sudo("pip3.4 install virtualenv")

def required_apt():
    apt = [
        "apache2",
        "libxml2 libxml2-dev",
        "libxslt1-dev libxslt1.1",
        "zlib1g-dev" # For XML etree
    ]
    python = [
        "python3.4",
        "python3.4-dev"
    ]

    #We check that python3-4 is available
    # Install required packages
    unable = sudo("apt-get install {0}".format(" ".join(apt + python)), warn_only=True)

    #Now we install virtualenv
    pip3 = str(run("pip3 --version", warn_only=True))
    if "3.4" in pip3:
        pip = "pip3"
    else:
        pip = "pip3.4"
    sudo("{0} install virtualenv".format(pip))

def prod():
    if env.available_hosts:
        env.hosts = env.available_hosts["prod"]["host"]
        env.user = env.available_hosts["prod"]["user"]
        env.remote_path = env.available_hosts["prod"]["remote_path"]
        env.remote_cache_path = env.available_hosts["prod"]["remote_cache_path"]


def stage():
    if env.available_hosts:
        env.hosts = env.available_hosts["stage"]["host"]
        env.user = env.available_hosts["stage"]["user"]
        env.remote_path = env.available_hosts["stage"]["remote_path"]
        env.remote_cache_path = env.available_hosts["stage"]["remote_cache_path"]


def get_version_stamp():
    "Get a dated and revision stamped version string"
    rev = str(local("git rev-parse --short HEAD", capture=True))
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    return "%s_%s" % (timestamp, rev)


def getPath():
    if env.version is None:
        env.version = get_version_stamp()
    return env.version


def makePath(target=None):
    if target is None:
        return '/'.join([env.remote_path, getPath()])
    else:
        return '/'.join([env.remote_path, getPath(), target])


def venv():
    # Create the virtual env in a flask folder.
    with cd(makePath()):
        run("virtualenv -p /usr/bin/python3.4 flask")


def check():
    version = re.compile("^Version:(\s\d\.\d.*)$", re.M)
    capture = run("dpkg -s libapache2-mod-wsgi-py3", warn_only=True)
    regexp = version.search(capture)
    try:
        if regexp.group(1):
            wsgi = True
        else:
            wsgi = False
    except:
        wsgi = False
    if wsgi is False:
        sudo("apt-get install libapache2-mod-wsgi-py3")


def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)


def deploy():
    check()
    pack()
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/yourapplication.tar.gz')
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    currentPath = makePath()
    run('mkdir -p ' + currentPath)
    with cd(currentPath):
        run('tar --strip-components=1 -zxvf /tmp/yourapplication.tar.gz')
        venv()
        # now setup the package with our virtual environment's
        # python interpreter
        with cd(makePath()):
            run(makePath("flask/bin/pip3.4") + " install -r requirements.txt")

            if "capitains-ahab" in modules["load"]:
                # There will be a git clone here
                run("git clone https://github.com/Capitains/Ahab.git")
                run(makePath("flask/bin/pip3.4") + " install -r Ahab/requirements.txt")

            if "joth" in modules["load"]:
                # There will be a git clone here
                run("git clone https://github.com/PerseusDL/perseids-client-apps-joth.git joth")