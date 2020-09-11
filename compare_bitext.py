import sys
import re

def normalize(x):
    x = re.sub("[^0-9A-Za-z\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7AF]", "", x)
    x = x.lower()
    return x

def filter(action, key, fn_txt, fn_ref):

    pool = {}
    fo_ref = open(fn_ref)
    for line in fo_ref:
        src, tgt = line.split("\t")
        src = normalize(src)
        tgt = normalize(tgt)
        pool[src] = True
        pool[tgt] = True
    fo_ref.close()

    num_sents = 0
    num_errors = 0

    fo_txt = open(fn_txt)
    for line in fo_txt:
        num_sents += 1

        if line.count("\t") != 1:
            num_errors += 1
            continue

        line = line.strip()
        src, tgt = line.split("\t")
        src = normalize(src)
        tgt = normalize(tgt)

        if src == "" or tgt == "":
            num_errors += 1
            continue

        if action == "dup":
            if key == "src" and src in pool:
                print(line)
                continue
            if key == "tgt" and tgt in pool:
                print(line)
                continue
            if key == "any" and (src in pool or tgt in pool):
                print(line)
                continue
            if key == "both" and (src in pool and tgt in pool):
                print(line)
                continue

        if action == "uniq":
            if key == "src" and src not in pool:
                print(line)
                continue
            if key == "tgt" and tgt not in pool:
                print(line)
                continue
            if key == "any" and (src not in pool or tgt not in pool):
                print(line)
                continue
            if key == "both" and (src not in pool and tgt not in pool):
                print(line)
                continue

    fo_txt.close()
    sys.stderr.write("%d sentences\n" % num_sents)
    sys.stderr.write("%d errors\n" % num_errors)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit("Usage: %s dup|uniq src|tgt|any|both text reference" % sys.argv[0])
    filter(*sys.argv[1:])
