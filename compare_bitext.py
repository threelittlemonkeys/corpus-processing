import sys
import re

def normalize(x):
    x = re.sub("[^0-9A-Za-z\u00C0-\u024F\u0400-\u04FF\u0E00-\u0E7F\u1E00-\u1EFF\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7AF]", "", x)
    x = x.lower()
    return x

def compare_bitext(action, key, flt, filename):

    pl = {}
    fo = open(filename)
    for line in fo:
        src, tgt = line.split("\t")
        if key == "norm":
            src = normalize(src)
            tgt = normalize(tgt)
        pl[src] = True
        pl[tgt] = True
    fo.close()

    num_sents = 0
    num_errors = 0

    for idx, line in enumerate(sys.stdin, 1):
        line = line.strip()

        if line.count("\t") != 1:
            num_errors += 1
            continue

        src, tgt = line.split("\t")
        if key == "norm":
            src = normalize(src)
            tgt = normalize(tgt)

        if src == "" or tgt == "":
            num_errors += 1
            continue

        flag = False

        if action == "dup":
            if flt == "src" and src not in pl:
                flag = True
            if flt == "tgt" and tgt in pl:
                flag = True
            if flt == "any" and (src in pl or tgt in pl):
                flag = True
            if flt == "both" and (src in pl and tgt in pl):
                flag = True

        if action == "uniq":
            if flt == "src" and src not in pl:
                flag = True
            if flt == "tgt" and tgt not in pl:
                flag = True
            if flt == "any" and (src not in pl or tgt not in pl):
                flag = True
            if flt == "both" and (src not in pl and tgt not in pl):
                flag = True

        if flag:
            print("%d\t%s" % (idx, line))
            num_sents += 1

    print("%d sentences in total" % idx, file = sys.stderr)
    print("%d sentences matched" % num_sents, file = sys.stderr)
    print("%d errors" % num_errors, file = sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 5 \
    or sys.argv[1] not in ("dup", "uniq") \
    or sys.argv[2] not in ("raw", "norm") \
    or sys.argv[3] not in ("src", "tgt", "any", "both"):
        sys.exit("Usage: %s dup|uniq raw|norm src|tgt|any|both ref < txt" % sys.argv[0])
    compare_bitext(*sys.argv[1:])
