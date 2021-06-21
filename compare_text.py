import sys
import re

def normalize(x):
    x = re.sub("[^0-9A-Za-z\u00C0-\u024F\u0400-\u04FF\u0E00-\u0E7F\u1E00-\u1EFF\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7AF]", "", x)
    x = x.lower()
    return x

def compare_text(action, key, filename):

    pl = {}
    fo = open(filename)
    for line in fo:
        norm = normalize(line) if key == "norm" else line
        pl[norm] = line
    fo.close()

    for line in sys.stdin:
        norm = normalize(line) if key == "norm" else line
        if action == "dup" and norm in pl:
            print(line, end = "")
        if action == "uniq" and norm not in pl:
            print(line, end = "")

if __name__ == "__main__":
    if len(sys.argv) != 4 \
    or sys.argv[1] not in ("dup", "uniq") \
    or sys.argv[2] not in ("raw", "norm"):
        sys.exit("Usage: %s dup|uniq raw|norm ref < txt" % sys.argv[0])
    compare_text(*sys.argv[1:])
