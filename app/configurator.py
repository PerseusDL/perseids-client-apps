from app.configurations.treebank import treebank
from app.configurations.session import session
from app.configurations.alignment import alignment
from app.configurations.annotation import annotation
from app.configurations.cts import cts
from app.configurations.language import language
from app.configurations.modules import modules


# Instead of json, we are going the py road so we can comment configurations and lessen the load time as well...
config = {}
config["treebank"] = treebank
config["alignment"] = alignment
config["annotation"] = annotation
config["session"] = session
config["cts"] = cts
config["language"] = language
config["modules"] = modules


def get(key):
    """
    @param  key  string  Key representing the subset of configurations concerned
    @type
    @returns function
    """
    return lambda s: config[key][s]
