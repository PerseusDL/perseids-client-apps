import json
from flask import Blueprint,  abort, request
import requests


ahab = Blueprint('capitains_ahab', __name__)
configuration = json.load(open("Ahab/configurations/cts.json"))


@ahab.route("/cts/xq", methods=["GET"])
def xq():
    try:
        r = requests.get(configuration["endpoint"], params=request.args.to_dict())
        if r.status_code != 200:
            abort(404)
        return r.text
    except:
        abort(404)
    abort(404)

"""
@ahab.route("/cts/rest/v1.0/search", methods=["GET"])
def xq():
    try:
        r = requests.get(configuration["search"], params=request.args.to_dict())
        if r.status_code != 200:
            abort(404)
        return r.text
    except:
        abort(404)
    abort(404)
"""
