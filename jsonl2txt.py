import sys
import re
import ast
import json

def normalize(line):
    line = re.sub("\s+", " ", line)
    line = line.strip()
    return line

def dump(obj, key = ""):

    if type(obj) in (int, float):
        print(key, obj, sep = "\t")

    if type(obj) == str:
        for txt in obj.split("\n"):
            txt = normalize(txt)
            if txt == "":
                continue
            print(key, txt, sep = "\t")

    if type(obj) == list:
        for e in obj:
            dump(e, key)

    if type(obj) == dict:
        for k, v in obj.items():
            dump(v, (key + "." if key else "") + k)

with open(sys.argv[1]) as fo:
    for line in fo:
        try:
            line = json.loads(line)
            dump(line)
        except:
            line = ast.literal_eval(line)
            dump(line)
