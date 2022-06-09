import sys
import re
import ast
import json

pl = dict()
RE_AL = re.compile("[A-Za-z\uAC00-\uD7AF]")

def normalize(line):
    line = re.sub("\s+", " ", line)
    line = line.strip()
    return line

def dump(obj):

    if type(obj) in (int, float):
        print(obj)
        return

    if type(obj) == str:
        for line in obj.split("\n"):
            line = normalize(line)
            if line == "":
                continue
            if not RE_AL.search(line):
                continue
            if line in pl:
                continue
            pl[line] = True
            print(line)
        return

    if type(obj) == list:
        for x in obj:
            dump(x)
        return

    if type(obj) == dict:
        for a, b in obj.items():
            print(a)
            dump(b)
        return

with open(sys.argv[1]) as fo:
    for line in fo:
        try:
            line = json.loads(line)
            dump(line)
        except:
            line = ast.literal_eval(line)
            dump(line)
