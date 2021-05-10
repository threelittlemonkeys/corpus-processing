import sys
import re

def normalize(x):
    x = re.sub("[^0-9A-Za-z\u00C0-\u024F\u0400-\u04FF\u0E00-\u0E7F\u1E00-\u1EFF\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7AF]", "", x)
    x = x.lower()
    return x

def compare_text(action, key, fn_txt, fn_ref):

    pool = {}
    fo_ref = open(fn_ref)
    for line in fo_ref:
        norm = normalize(line) if key == "norm" else line
        pool[norm] = line
    fo_ref.close()

    fo_txt = open(fn_txt)
    for line in fo_txt:
        norm = normalize(line) if key == "norm" else line
        if action == "dup" and norm in pool:
            print(line, end = "")
        if action == "uniq" and norm not in pool:
            print(line, end = "")
    fo_txt.close()

if __name__ == "__main__":
    if len(sys.argv) != 5 \
    or sys.argv[1] not in ("dup", "uniq") \
    or sys.argv[2] not in ("raw", "norm"):
        sys.exit("Usage: %s dup|uniq raw|norm text reference" % sys.argv[0])
    compare_text(*sys.argv[1:])
