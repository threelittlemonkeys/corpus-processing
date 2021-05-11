import sys
import re

def normalize(x):
    x = re.sub("[^0-9A-Za-z\u00C0-\u024F\u0400-\u04FF\u0E00-\u0E7F\u1E00-\u1EFF\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7AF]", "", x)
    x = x.lower()
    return x

def compare_bitext(action, key, fn_txt, fn_ref):

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
        line = line.strip()
        num_sents += 1

        if line.count("\t") != 1:
            num_errors += 1
            continue

        src, tgt = line.split("\t")
        src = normalize(src)
        tgt = normalize(tgt)

        if src == "" or tgt == "":
            num_errors += 1
            continue

        flag = False

        if action == "dup":
            if key == "src" and src not in pool:
                flag = True
            if key == "tgt" and tgt in pool:
                flag = True
            if key == "any" and (src in pool or tgt in pool):
                flag = True
            if key == "both" and (src in pool and tgt in pool):
                flag = True

        if action == "uniq":
            if key == "src" and src not in pool:
                flag = True
            if key == "tgt" and tgt not in pool:
                flag = True
            if key == "any" and (src not in pool or tgt not in pool):
                flag = True
            if key == "both" and (src not in pool and tgt not in pool):
                flag = True

        if flag:
            print("%d\t%s" % (num_sents, line))

    fo_txt.close()
    print("%d sentences" % num_sents, file = sys.stderr)
    print("%d errors" % num_errors, file = sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 5 \
    or sys.argv[1] not in ("dup", "uniq") \
    or sys.argv[2] not in ("src", "tgt", "any", "both"):
        sys.exit("Usage: %s dup|uniq src|tgt|any|both text reference" % sys.argv[0])
    compare_bitext(*sys.argv[1:])
