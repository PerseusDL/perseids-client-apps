from flask import Flask
from flask.ext.babel import Babel
from flask_bower import Bower


app = Flask(__name__)
babel = Babel(app)
bower = Bower(app)

from app import views
