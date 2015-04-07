from fabric.api import *
from fabconf import user, hosts
import re

# the user to use for the remote commands
env.user = user
# the servers where the commands are executed
env.hosts = hosts


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
    run('mkdir /tmp/yourapplication')
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
