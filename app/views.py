# coding=utf8

from app import app
from app import configurator
from app import babel
from app import bower
from flask import render_template, request, jsonify, session, redirect, url_for
from flask_oauthlib.client import OAuth
from functools import wraps
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

@app.route('/oauth_login')
def r_oauth_login(next=None):
    """
    Route for OAuth2 Login

    :param next next url
    :type str

    :return: Redirects to OAuth Provider Login URL
    """
    session['next'] = next
    callback_url = configurator.get("oauth")("callback_url")
    if callback_url is None:
        callback_url = url_for('r_oauth_authorized', _external=True)
    return get_authobj().authorize(callback=callback_url)

@app.route('/oauth_authorized')
def r_oauth_authorized():
    """
    Route for OAuth2 Authorization callback
    :return: {"template"}
    """
    authobj = get_authobj()
    resp = authobj.authorized_response()
    if resp is None:
         return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
         )
    session['oauth_token'] = (resp['access_token'], '')
    user = authobj.get('user')
    ## TODO this is too specific to Perseids' api model. We should externalize.
    session['oauth_user_uri'] = user.data['user']['uri']
    session['oauth_user_name'] = user.data['user']['full_name']
    if 'next' in session and session['next'] is not None:
        return redirect(session['next'])
    else:
        return render_template(
            'oauth/user.html',
            user_name=user.data['user']['full_name']
        )

def oauth_token(token=None):
    """
    tokengetter function
    :return: the current access token
    :rtype str
    """
    return session.get('oauth_token')

def oauth_required(f):
    """
    decorator to add to a view to require an oauth user
    :return: decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'oauth_user_uri' not in session or session['oauth_user_uri'] is None:
            return redirect(url_for('.r_oauth_login', next=request.url))
        return f(*args,**kwargs)
        return decorated_function

def get_authobj():
    oauth = OAuth(app)
    auth_config = configurator.get("oauth")
    authobj = oauth.remote_app(
        auth_config("name"),
        consumer_key=auth_config("key"),
        consumer_secret=auth_config("secret"),
        request_token_params={'scope':auth_config("scope")},
        base_url=auth_config("base_api_url"),
        request_token_url=auth_config("request_token_url"),
        access_token_method='POST',
        access_token_url=auth_config("access_token_url"),
        authorize_url=auth_config("authorize_url")
    )
    authobj.tokengetter(oauth_token)
    return authobj

