# coding=utf8

from app import app
from app import configurator
from app import babel
from app import bower
from flask import render_template, request, jsonify, flash, redirect, url_for, session
from os.path import expanduser

HOME = expanduser("~")
app.secret_key = 'adding this in so flash messages will work'

import sys
import json


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

@app.route('/save_data', methods=['GET', 'POST'])
def save_data():
    if request.method == 'POST':
      data_dict = request.get_json()
      data = json.dumps(data_dict, indent=2, sort_keys=True)
      raw_id = data_dict['commentary'][0]['hasBody']['@id'].encode()
      mil_id = raw_id.split(':').pop()
      path = "/digmil/"+mil_id+".txt"
      session['path'] = path
      session['data'] = data
      with open(HOME+path, "wb") as mil_file:
        mil_file.write(data)
      return render_template('save_data/success.html', path=path, data=data)
    else:     
      path = session['path']
      data = session['data']
      return render_template('save_data/success.html', path=path, data=data)
    