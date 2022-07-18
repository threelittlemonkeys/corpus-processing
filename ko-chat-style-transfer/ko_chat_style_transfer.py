import os
import sys
import re
import xre
import random

PATH = (os.path.dirname(__file__) or ".") + "/"
RE_TOKEN = re.compile("[가-힣]+")

def load_dict(filename, dtype):
    do = {}
    syms = {}
    fo = open(filename)

    for ln, line in enumerate(fo, 1):

        # preprocessing

        line = re.sub("#.*", "", line)
        line = re.sub("\s*\t\s*", "\t", line)
        line = line.strip()

        if line == "":
            continue
        if line == "<EOF>":
            break

        # symbols

        m = re.search("^<([^ >]+)> = (<[^ >]+>(?: \+ <[^ >]+>)+)", line)
        if m:
            k, vs = m.groups()
            v = "(%s)" % "|".join([syms[v[1:-1]] for v in vs.split(" + ")])
            syms[k] = v
            continue

        m = re.search("^<([^ >]+)> = (.+)$", line)
        if m:
            k, v = m.groups()
            syms[k] = v
            continue

        try:
            item = re.sub("<(.+?)>", lambda x: "(%s)" % syms[x.group(1)], line)
        except:
            sys.exit("Error: unknown symbol at line %d" % ln)

        # load dictionary items

        try:
            x, y = item.split("\t")
        except:
            sys.exit("Error: invalid format at line %d" % ln)

        if dtype == re:
            x = re.compile(x)

        if x not in do:
            do[x] = []
        elif y in do[x]:
            sys.exit("Error: item already exists at line %d" % ln)
        do[x].append((y, line))

    fo.close()
    return do

def ko_chat_style_transfer(line):
    k = 0
    ls = []
    out = line

    for m in RE_TOKEN.finditer(line):
        w, i, j = m.group(), m.start(), m.end()
        cands = [(w, [])]

        if w in lex_dict:
            for y, r in lex_dict[w]:
                cands.append((y, [r]))

        for pt in rex_dict:
            for x, rs in list(cands):
                if not pt.search(x):
                    continue
                for y, r in rex_dict[pt]:
                    cands.append((xre.sub(pt, y, x), rs + [r]))

        if len(cands) > 1:
            ys = [y for y, _ in cands]
            y, rs = random.choice(cands)
            ls.append((w, y, rs, ys))
            out = out[:i + k] + y + out[j + k:]
            k += len(y) - (j - i)

    return ls, out

if __name__ == "__main__":

    if len(sys.argv) not in (2, 3):
        sys.exit("Usage: %s all|diff|same [-v] < txt" % sys.argv[0])

    op = sys.argv[1]
    verbose = (len(sys.argv) == 3 and sys.argv[2] == "-v")

    lex_dict = {}
    rex_dict = load_dict(PATH + "ko_chat_style_dict.tsv", re)

    for line in sys.stdin:

        ls, out = ko_chat_style_transfer(line)

        if op == "all" \
        or op == "diff" and line != out \
        or op == "same" and line == out:
            print(out, end = "")

        if verbose:
            i = 0
            for w, y, rs, ys in ls:
                if w == y:
                    continue
                print(f"[{i}]", ys)
                print("->", (w, y))
                for j, r in enumerate(rs):
                    print(f"   [{j}]", *r.split("\t"))
                print()
                i += 1
