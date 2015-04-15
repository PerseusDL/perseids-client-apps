import json
from flask import Blueprint, request, jsonify, render_template, make_response
import glob

joth = Blueprint('joth', __name__, template_folder='templates')
dataFolder = "./JOTH/data/"


def getAnnotations(key):
    """
      Get Annotations for a specific kind of data.
        Create cache
    """
    jsons = glob.glob(dataFolder + key + "/*.json")
    cachePath = dataFolder + key + ".json"
    try:
        current = json.load(open(cachePath))
    except:
        current = {
            key: []
        }
    if len(jsons) != len(current[key]):
        for path in jsons:
            with open(path) as file_:
                current[key].append(json.load(file_))
        # We write the cache
        with open(cachePath, 'w') as outfile:
            json.dump(current, outfile)
    return current


@joth.route("/joth/places", methods=["GET"])
def placesCtrl():
    urn = request.args.get("urn") or "noURN"
    places = getAnnotations("places")
    return jsonify({"places": [place for place in places["places"] if place["hasTarget"]["hasSource"]["@id"].startswith(urn)]})


@joth.route("/joth/books/reffs")
def bookCtrl():
    urn = request.args.get("urn")

    annots = [annot for annot in getAnnotations("places")["places"]]
    annots = annots + [annot for annot in getAnnotations("persons")["persons"]]
    annots = annots + [annot for annot in getAnnotations("occurences")["occurences"]]
    print(annots[0])

    urns = [annot["hasTarget"]["hasSource"]["@id"] for annot in annots if annot["hasTarget"]["hasSource"]["@id"].startswith(urn)]
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
def booksCtrl():
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


@joth.route("/joth/pleiades", methods=["GET", "POST"])
@joth.route("/joth/pleiades/<place>", methods=["GET"])
def pleiadesCtrl(place=None):
    if not place:
        req = request.args.get("places").split(",")
    else:
        req = [place]
    req = list(set(req))
    places = {}
    for placeId in req:
        places[placeId] = {}
        try:
            with open("./JOTH/pleiades/{0}.geojson".format(placeId)) as f:
                places[placeId] = json.load(f)
        except:
            print("This does not exist")
    return jsonify({"places": places})


@joth.route("/joth/persons", methods=["GET"])
def personsCtrl():
    urn = request.args.get("urn") or "noURN"
    resources = getAnnotations("persons")
    return jsonify({"persons" : [person for person in resources["persons"] if person["hasTarget"]["hasSource"]["@id"].startswith(urn)]})
