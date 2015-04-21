import os
import sys
import site

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

# Activate your virtual env
from wsgivenv import activate_venv
activate_venv(os.path.dirname(os.path.abspath(__file__)))

# We run the app
from app import app as application
