from app.configurations.treebank import treebank
from app.configurations.session import session
from app.configurations.alignment import alignment
from app.configurations.cts import cts
from app.configurations.language import language


# Instead of json, we are going the py road so we can comment configurations and lessen the load time as well...
config = {}
config["treebank"] = treebank
config["alignment"] = alignment
config["session"] = session
config["cts"] = cts
config["language"] = language


def get(key):
    """
    @param  key  string  Key representing the subset of configurations concerned
    @type
    @returns function
    """
    return lambda s: config[key][s]
