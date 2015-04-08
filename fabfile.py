from fabric.api import *
from fabconf import user, hosts, path, available_hosts
from fabvenv import make_virtualenv
from datetime import datetime
import re

# the user to use for the remote commands
env.user = user
# the servers where the commands are executed
env.hosts = hosts
env.remote_path = path
env.version = None


TIMESTAMP_FORMAT = "%Y%m%d%H%M%S"


def prod():
    if env.available_hosts:
        env.hosts = env.available_hosts["prod"]["host"]
        env.user = env.available_hosts["prod"]["user"]
        env.remote_path = env.available_hosts["prod"]["remote_path"]
        env.remote_cache_path = env.available_hosts["prod"]["cache_path"]


def stage():
    if env.available_hosts:
        env.hosts = env.available_hosts["stage"]["host"]
        env.user = env.available_hosts["stage"]["user"]
        env.remote_path = env.available_hosts["stage"]["remote_path"]
        env.remote_cache_path = env.available_hosts["stage"]["cache_path"]


def get_version_stamp():
    "Get a dated and revision stamped version string"
    rev = str(local("git rev-parse --short HEAD", capture=True))
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    return "%s_%s" % (timestamp, rev)


def getPath():
    if env.version is None:
        env.version = get_version_stamp()
    return env.version


def makePath(target):
    return '/'.join([env.remote_path, getPath(), target])


def venv():
    # Create the virtual env in a flask folder.
    make_virtualenv(makePath("/flask"), dependencies=[
        "Flask==0.10.1",
        "Flask-Babel==0.9",
        "Flask-Bower==1.0.1"
    ], system_site_packages=True)


def check():
    version = re.compile("^Version:(\s\d\.\d.*)$", re.M)
    capture = str(run("dpkg -s libapache2-mod-wsgi"))
    regexp = version.search(capture)
    try:
        if regexp.group(1):
            wsgi = True
        else:
            wsgi = False
    except:
        wsgi = False
    if wsgi is False:
        sudo("apt-get install libapache2-mod-wsgi")


def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)


def deploy():
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/yourapplication.tar.gz')
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir -p /tmp/yourapplication')
    with cd('/tmp/yourapplication'):
        run('tar xzf /tmp/yourapplication.tar.gz')
        # now setup the package with our virtual environment's
        # python interpreter
        run('/var/www/yourapplication/env/bin/python setup.py install')
    # now that all is set up, delete the folder again
    run('rm -rf /tmp/yourapplication /tmp/yourapplication.tar.gz')
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    run('touch /var/www/yourapplication.wsgi')
