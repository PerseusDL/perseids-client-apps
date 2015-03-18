from flask import Flask
from flask.ext.babel import Babel
from flask_bower import Bower
from flask import config

app = Flask(__name__)
bower = Bower(app)
from app import views
