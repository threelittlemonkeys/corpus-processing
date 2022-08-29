import sys
import re
import csv

def normalize(txt):
    txt = re.sub("\r", "\\n", txt)
    txt = re.sub("\s+", " ", txt)
    txt = txt.strip()
    return txt

with open(sys.argv[1]) as fo:
    data = csv.reader(fo)
    for row in data:
        cols = [normalize(col) for col in row]
        print(*cols, sep = "\t")
