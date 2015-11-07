from flask import Flask
from flask.ext.babel import Babel
from flask_bower import Bower
from app import configurator
from app.cache import cache
from flask.ext.cors import CORS
from flask.ext.pymongo import PyMongo

app = Flask(__name__, template_folder="templates")
cors = CORS(app)
babel = Babel(app)
bower = Bower(app)
mongo = PyMongo(app)
load = configurator.get("modules")("load")
cache.init_app(app,config={'CACHE_TYPE': 'simple'})

from app import views
