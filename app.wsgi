import os, sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

activate = path + '/flask/bin/activate_this.py'
execfile(activate, dict(__file__=activate))

from app import app as application