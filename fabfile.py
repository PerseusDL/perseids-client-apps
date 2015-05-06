from fabric.api import *
from fabconf import available_hosts
from datetime import datetime
import re
from StringIO import StringIO

# List of conf folder and their equivalencies in the deployed folder
confFiles = {
    # "Conf Original Folder" : ".conf Equivalency folder"
    "Ahab/configurations" : "/ahab",
    "app/configurations" : "/main",
}
# List of data folder and their equivalencies in the deployed folder
dataFiles = {
    "joth/data" : "/joth",
    "joth/pleiades" : "/pleiades-geojson/geojson"
}

# Bad and hacky but only way to avoid __init__.py issues
try:
    execfile(".conf" + confFiles["app/configurations"] +"/modules.py")
except:
    import sys
    sys.exit("Remote configurations files not available in ./conf")

env.version = None
env.available_hosts = available_hosts
TIMESTAMP_FORMAT = "%Y%m%d%H%M%S"

@task
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


@task
def required_apt():
    """ Install required app for remote machine with Ubuntu > 12.04  """
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


@task
def prod():
    """ Prefix any command to deploy to prod server """
    if env.available_hosts:
        env.hosts = env.available_hosts["prod"]["host"]
        env.user = env.available_hosts["prod"]["user"]
        env.apacheuser = env.available_hosts["prod"]["apache-runner"]
        env.remote_path = env.available_hosts["prod"]["remote_path"]
        env.remote_cache_path = env.available_hosts["prod"]["remote_cache_path"]
        env.pipcache = env.available_hosts["prod"]["remote_pip_cache"]
        env.confpath = env.available_hosts["prod"]["remote_conf_path"]
        env.datapath = env.available_hosts["prod"]["remote_data_path"]
        env.venv = env.available_hosts["prod"]["remote_venv_path"]
        env.wsgi = env.available_hosts["prod"]["remote_wsgi_path"]


@task
def stage():
    """ Prefix any command to deploy to stage server """
    if env.available_hosts:
        env.hosts = env.available_hosts["stage"]["host"]
        env.user = env.available_hosts["stage"]["user"]
        env.apacheuser = env.available_hosts["stage"]["apache-runner"]
        env.remote_path = env.available_hosts["stage"]["remote_path"]
        env.remote_cache_path = env.available_hosts["stage"]["remote_cache_path"]
        env.pipcache = env.available_hosts["stage"]["remote_pip_cache"]
        env.confpath = env.available_hosts["stage"]["remote_conf_path"]
        env.datapath = env.available_hosts["stage"]["remote_data_path"]
        env.venv = env.available_hosts["stage"]["remote_venv_path"]
        env.wsgi = env.available_hosts["stage"]["remote_wsgi_path"]


def get_version_stamp():
    "Get a dated and revision stamped version string"
    rev = str(local("git rev-parse --short HEAD", capture=True))
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    return "%s_%s" % (timestamp, rev)


def getPath():
    if env.version is None:
        env.version = get_version_stamp()
    return env.version


def simplePath(target):
    return '/'.join([env.remote_path, target])


def makePath(target=None):
    if target is None:
        return '/'.join([env.remote_path, getPath()])
    else:
        return '/'.join([env.remote_path, getPath(), target])


def venv():
    """ Create a virtual env """
    # Create the virtual env in a flask folder.

    run("virtualenv -p /usr/bin/python3.4 " + env.venv, warn_only=True, quiet=True)


def check():
    """ Check That MOD WSGI PY3 is installed """

    # THIS PART IS HIGLY CONTROVERSIAL...
    # sudo("rm /usr/bin/python3; ln -s /usr/bin/python3.4 /usr/bin/python3")
    # This is less
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


@task
def pack():
    """ Pack up main app and modules if required """
    # If we have to get Capitains ahab...
    if "capitains-ahab" in modules["load"]:
        local("rm -rf Ahab", capture=False)
        local("git clone https://github.com/Capitains/Ahab.git Ahab", capture=False)
    # If we have to get Joth Modules...
    if "joth" in modules["load"]:
        local("rm -rf joth", capture=False)
        local("git clone https://github.com/PerseusDL/perseids-client-apps-joth.git joth", capture=False)
    local("cd app ; bower install; cd ../", capture=False)
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)


@task
def deploy_conf():
    """ Deploy configurations files on remote server """
    try:
        local('rm conf.tar',capture=False)
    except:
        pass
    local("tar -zcvf conf.tar .conf",capture=False) # Create the zip of conf folder
    put('conf.tar', '/tmp/conf.tar') # Send the conf to remote server
    run('mkdir -p {0}'.format(env.confpath), warn_only=True, quiet=True)
    run('tar -zcvf {0}.tar {0}'.format(env.confpath), warn_only=True) # Backup the current conf
    run('rm -rf {0}/*'.format(env.confpath), warn_only=True, quiet=True) # Remove old conf
    run('tar --strip-components=1 -zxvf /tmp/conf.tar -C {0}'.format(env.confpath)) # Untar new conf


@task
def rollback_conf():
    """ Rollback the last config available on remote server """
    run('rm -rf {0}/*'.format(env.confpath)) # Remove current conf
    run('tar --strip-components=1 -zxvf {0}.tar -C {0}'.format(env.confpath)) # Untar backup

    return True


@task
def update_conf(version):
    """ Update the sym links between the app and the main conf """
    currentPath = simplePath(version)
    with cd(currentPath):
        for key in confFiles:
            run("rm -rf {0}".format(key), warn_only=True, quiet=True)
            run("ln -s {source} {target}".format(source=env.confpath + confFiles[key], target=currentPath + "/" + key))


@task
def update_data(version):
    """ Update the sym links between the app and the data directories """
    currentPath = simplePath(version)
    with cd(currentPath):
        for key in dataFiles:
            run("rm {0}".format(key), warn_only=True, quiet=True)
            run("ln -s {source} {target}".format(source=env.datapath + dataFiles[key], target=currentPath + "/" + key))


@task
def wsgi(version):
    put(StringIO(
    '''
import os
import sys

# We run the app
sys.path.append(\"{0}\")
from app import app as application
'''.format(simplePath(version))), env.wsgi)


@task
def deploy():
    """ Deploy latest version to the distant machine """
    # check()
    pack()
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/app.tar.gz')
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    currentPath = makePath()
    run('mkdir -p ' + currentPath)
    run('mkdir -p ' + env.pipcache)
    with cd(currentPath):
        run('tar --strip-components=1 -zxvf /tmp/app.tar.gz', quiet=True)
        venv()
        # now setup the package with our virtual environment's
        # python interpreter
        with cd(makePath()):
            run("{0}/bin/pip3.4 install -r requirements.txt".format(env.venv), quiet=True)
            if "capitains-ahab" in modules["load"]: # We need to install the requirements from AHAB
                run("{0}/bin/pip3.4 install -r Ahab/requirements.txt".format(env.venv))

    version = currentPath.split("/")[-1]
    update_conf(version)
    update_data(version)
    sudo("chown -R {0} {1}".format(env.apacheuser, currentPath))
    wsgi(version)
    print("Last version " + currentPath)
    print("Run : \n{0}/bin/python3.4 {1}/run.py".format(env.venv, currentPath))


@task
def releases(p=True):
    """List a releases made"""
    env.releases = sorted([line for line in run('ls -tx %(releases_path)s' % { 'releases_path':env.remote_path }).split() if "wsgi" not in line])
    if len(env.releases) >= 1:
        env.current_revision = env.releases[0]
        env.current_release = "%(releases_path)s/%(current_revision)s" % { 'releases_path':env.remote_path, 'current_revision':env.current_revision }
    if len(env.releases) > 1:
        env.previous_revision = env.releases[1]
        env.previous_release = "%(releases_path)s/%(previous_revision)s" % { 'releases_path':env.remote_path, 'previous_revision':env.previous_revision }
    if p:
        print(env.releases)


@task
def rollback(version=None):
    if not version:
        releases(False)
        print(version)
        wsgi(env.previous_revision)
    else:
        wsgi(version)
