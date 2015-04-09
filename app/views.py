from app import app
from app import configurator
from app import babel
from flask import render_template, request, jsonify


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(configurator.get("language")("available").keys())


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


@app.route('/alignment')
def alignment():
    return render_template(
       'alignment/enter.html',
       alignment=configurator.get("alignment"),
       session=configurator.get("session"),
       cts=configurator.get("cts")
     )


@app.route("/joth/books")
def books():
    return jsonify({
        "books": [
          {
              "id": "urn:cts:pdlrefwk:viaf88890045.003.perseus-eng1",
              "title": "Dictionary of Greek and Roman Geography",
              "uri": "http://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0104",
              "author": "W-Smith"
          }
        ]
      }
      )
