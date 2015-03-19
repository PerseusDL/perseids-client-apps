import json
from flask import Blueprint,  abort, request
import requests


ahab = Blueprint('capitains_ahab', __name__)
configuration = json.load(open("Ahab/configurations/cts.json"))


@ahab.route("/xq", methods=["GET"])
def xq():
    try:
        r = requests.get(configuration["endpoint"], params=request.args.to_dict())
        if r.status_code != 200:
            abort(404)
        return r.text
    except:
        abort(404)
    abort(404)
