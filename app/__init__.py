from flask import Flask
from flask.ext.babel import Babel
from flask_bower import Bower
from flask_cors import CORS


app = Flask(__name__)
babel = Babel(app)
bower = Bower(app)
cors = CORS(app)

from app import views
