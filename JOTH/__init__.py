import json
from flask import Blueprint, request, jsonify, render_template, make_response

joth = Blueprint('joth', __name__, template_folder='templates')
places = json.load(open("JOTH/data/places.json"))


@joth.route("/joth/places", methods=["GET"])
def xq():
    urn = request.args.get("urn")
    return jsonify({"places": [place for place in places["places"] if place["hasTarget"]["hasSource"]["@id"].startswith(urn)]})


@joth.route("/joth/books/reffs")
def book():
    urn = request.args.get("urn")
    urns = [place["hasTarget"]["hasSource"]["@id"] for place in places["places"] if place["hasTarget"]["hasSource"]["@id"].startswith(urn)]
    urns = list(set(urns))
    responseXml = render_template(
        'getValidReff.xml',
        urn=request.args.get("urn"),
        results=urns
    )
    response = make_response(responseXml)
    response.headers["Content-Type"] = "application/xml"
    return response


@joth.route("/joth/books")
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
