from flask import Flask
from flask.ext.babel import Babel
from flask_bower import Bower
from app import configurator
from app.cache import cache
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app)
babel = Babel(app)
bower = Bower(app)
load = configurator.get("modules")("load")
cache.init_app(app)

if "capitains-ahab" in load:
    from Ahab import ahab
    app.register_blueprint(ahab)


from JOTH import joth
app.register_blueprint(joth)


from app import views
