import glob
import re

urn = re.compile("(urn:cts:pdlrefwk:viaf88890045\.003\.perseus-eng1:)([a-zA-Z]{1})", re.MULTILINE)
jsons = glob.glob("./*/*.json")
def fn(matchobj):
    return matchobj.group(1) + matchobj.group(2).upper() + "." + matchobj.group(2)

for json in jsons:
    with open(json) as f:
        text = f.read()
        text = urn.sub(fn, text)
        f.close()
    with open(json, "w") as f:
        f.write(text)
        f.close()
