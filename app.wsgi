import os
import sys
import site

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(path + '/flask/lib/python3.4/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append(path)

# os.environ['SETTINGS ?'] = 'myproject.settings'

# Activate your virtual env
activate_env = os.path.expanduser(path + "/flask/bin/activate_this.py")
with open(activate_env) as f:
    code = compile(f.read(), activate_env, 'exec')
    exec(code, dict(__file__=activate_env))

# We run the app
from app import app as application
