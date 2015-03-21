import json
from flask import Blueprint,  abort, request
import requests
import requests_cache
from lxml import etree

ahab = Blueprint('capitains_ahab', __name__)
configuration = json.load(open("Ahab/configurations/cts.json"))
if configuration["cache"]:
    requests_cache.install_cache("capitains-ahab", backend="sqlite", expire_after=configuration["cache.time"])


def requesting(endpoint, params):
    try:
        r = requests.get(endpoint, params=params)
        print(params)
        if r.status_code != 200:
            abort(404)
        return r.text
    except:
        abort(404)
    abort(404)


def makeUrn(namespace, work=None):
    if work is not None and len(work) > 0:
        return "urn:cts:{0}:{1}".format(namespace, ".".join(work))
    else:
        return "urn:cts:{0}".format(namespace)


@ahab.route("/cts/api", methods=["GET"])
def xq():
    return requesting(configuration["endpoint"], params=request.args.to_dict())


"""
RESTful API
"""
if configuration["restfull"] is True:
    @ahab.route("/cts/rest/v1.0/<inventory>", methods=["GET"])
    def getCapabilities(inventory):
        return requesting(configuration["endpoint"], params={"request": "GetCapabilities", "inv": inventory})

    @ahab.route("/cts/rest/v1.0/<inventory>/<namespace>", methods=["GET"])
    def getNamespaceCapabilities(inventory, namespace):
        return requesting(configuration["endpoint"], params={
            "request": "GetCapabilities",
            "inv": inventory,
            "urn": makeUrn(namespace)
        })

    @ahab.route("/cts/rest/v1.0/<inventory>/<namespace>/<textgroup>", methods=["GET"])
    def getTextGroupCapabilities(inventory, namespace, textgroup):
        return requesting(configuration["endpoint"], params={
            "request": "GetCapabilities",
            "inv": inventory,
            "urn": makeUrn(namespace, [textgroup])
        })

    @ahab.route("/cts/rest/v1.0/<inventory>/<namespace>/<textgroup>/<work>", methods=["GET"])
    def getWorkCapabilities(inventory, namespace, textgroup, work):
        return requesting(
            configuration["endpoint"],
            params={
                "request": "GetCapabilities",
                "inv": inventory,
                "urn": makeUrn(namespace, [textgroup, work])
            }
        )

    @ahab.route("/cts/rest/v1.0/<inventory>/<namespace>/<textgroup>/<work>/<text>/validReff", methods=["GET"])
    def getWorkValidReff(inventory, namespace, textgroup, work, text):
        return requesting(
            configuration["endpoint"],
            params={
                "request": "GetValidReff",
                "inv": inventory,
                "urn": "urn:cts:{0}:{1}.{2}.{3}".format(namespace, textgroup, work, text),
                "level": request.args.get("level")
            }
        )

    @ahab.route("/cts/rest/v1.0/<inventory>/<namespace>/<textgroup>/<work>/<text>/passage/<ref>", methods=["GET"])
    def getWorkPassage(inventory, namespace, textgroup, work, text, ref):
        return requesting(
            configuration["endpoint"],
            params={
                "request": "GetPassage",
                "inv": inventory,
                "urn": "urn:cts:{0}:{1}.{2}.{3}:{4}".format(namespace, textgroup, work, text, ref),
                "level": request.args.get("level")
            }
        )

    @ahab.route("/cts/rest/v1.0/<inventory>/<namespace>/<textgroup>/<work>/<text>/passagePlus/<ref>", methods=["GET"])
    def getWorkPassagePlus(inventory, namespace, textgroup, work, text, ref):
        return requesting(
            configuration["endpoint"],
            params={
                "request": "GetPassagePlus",
                "inv": inventory,
                "urn": "urn:cts:{0}:{1}.{2}.{3}:{4}".format(namespace, textgroup, work, text, ref),
                "level": request.args.get("level")
            }
        )

    @ahab.route("/cts/rest/v1.0/<inventory>/<namespace>/<textgroup>/<work>/<text>/firstPassage", methods=["GET"])
    def getWorkFirstPassage(inventory, namespace, textgroup, work, text):
        return requesting(
            configuration["endpoint"],
            params={
                "request": "GetFirstPassage",
                "inv": inventory,
                "urn": "urn:cts:{0}:{1}.{2}.{3}:{4}".format(namespace, textgroup, work, text),
                "level": request.args.get("level")
            }
        )

if "ahab.search" in configuration:
    @ahab.route("/ahab/rest/v1.0/search", methods=["GET"])
    def search():
        params = request.args.to_dict().copy()
        params.update({"request": "Search"})

        return requesting(
            configuration["ahab.endpoint"],
            params=params
        )

if "ahab.permalink" in configuration:
    @ahab.route("/ahab/rest/v1.0/permalink/<ref>", methods=["GET"])
    def permalink(ref):
        r = requests.get(configuration["ahab.endpoint"], params={"request": "permalink", "urn": ref})
        xml = etree.fromstring(r.text)
        if r.status_code != 200:
            abort(404)
        return requesting(
            configuration["endpoint"],
            params={"request": "GetPassagePlus", "urn": ref, "inv": xml.find(".//ahab:inventory", {"ahab": "http://github.com/capitains/ahab"}).text}
        )
