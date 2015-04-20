import os, sys, site

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(path + '/flask/lib/python3.4/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append(path)

# Activate your virtual env
activate_env = os.path.expanduser(path + "/flask/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from app import app as application
