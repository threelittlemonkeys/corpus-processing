import os
import sys
import re
import xre
import random

PATH = (os.path.dirname(__file__) or ".") + "/"
RE_TOKEN = re.compile("[가-힣]+")

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

        for pt in xre_dict:
            for x, rs in list(cands):
                if not pt.search(x):
                    continue
                for y, r in xre_dict[pt]:
                    cands.append((xre.sub(pt, y, x), rs + [r]))

        if len(cands) > 1:
            ys = [y for y, _ in cands]
            y, rs = random.choice(cands[1:])
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
    xre_dict = xre.read(PATH + "ko_chat_style_transfer_dict.xre")

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
