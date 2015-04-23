import os
import sys

# We run the app
from app import app as application

application.config['DEBUG'] = True