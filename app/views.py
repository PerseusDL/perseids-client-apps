from app import app
from app import configurator
from flask import render_template
from app.config import LANGUAGES


"""@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())
"""

@app.route('/')
@app.route('/index')
def index():
    return "Nothing to see here !"


@app.route('/treebank')
def treebank():
    return render_template(
       'treebank/enter.html',
       treebank=configurator.get("treebank"),
       session=configurator.get("session"),
       cts=configurator.get("cts")
     )
