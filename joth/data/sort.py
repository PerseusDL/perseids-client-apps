import glob
import os

jsons = glob.glob("./*.json")
try:
    os.makedirs("./persons")
except:
    print("Persons exists already")
try:
    os.makedirs("./places")
except:
    print("Places exists already")
try:
    os.makedirs("./occurences")
except:
    print("Occurences exists already")

for json in jsons:
    path = "./"
    with open(json) as f:
        text = f.read()
        if "http://lawd.info/ontology/Attestation" in text:
            path = "./occurences/" + json
        elif "snap:has-bond" in text:
            path = "./persons/" + json
        elif "pleiades.stoa.org" in text:
            path = "./places/" + json
        f.close()
    try:
        os.rename(json, path)
    except:
        print("Unable to move {0} to {1}".format(json, path))