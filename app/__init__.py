from flask import Flask
from flask.ext.babel import Babel
from flask_bower import Bower
from app import configurator
from app.cache import cache

app = Flask(__name__)
babel = Babel(app)
bower = Bower(app)
load = configurator.get("modules")("load")
cache.init_app(app)

if "capitains-ahab" in load:
    from Ahab import ahab
    app.register_blueprint(ahab)


from app import views
