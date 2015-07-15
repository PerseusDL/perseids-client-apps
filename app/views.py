# coding=utf8

from app import app
from app import configurator
from app import babel
from app import bower
from flask import render_template, request, jsonify
import sys


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

@app.route('/thematic')
def thematic():
    return render_template(
     'treebank/theme.html',
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

@app.route('/annotation')
def annotation():
    return render_template(
       'annotation/enter.html',
       annotation=configurator.get("annotation"),
       session=configurator.get("session"),
       cts=configurator.get("cts")
     )    
