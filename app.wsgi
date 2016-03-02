import os
import sys

sys.path.insert(0, '/var/www/perseids-client-apps')

# We run the app
from app import app as application
print(sys.version)
application.config['DEBUG'] = True
