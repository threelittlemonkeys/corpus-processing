import os
import sys
import re
import random
sys.path.append("../xre")
import xre

class ko_chat_style_transfer():

    def __init__(self, lex_dict, xre_dict, verbose):
        self.lex_dict = {}
        self.xre_dict = xre.read(xre_dict)
        self.verbose = verbose

        self.re_token = re.compile("[가-힣]+")

    def transfer(self, line):
        k = 0
        ls = []
        out = line

        for m in self.re_token.finditer(line):
            w, i, j = m.group(), m.start(), m.end()
            cands = [(w, [])]

            if w in self.lex_dict:
                for y, r in self.lex_dict[w]:
                    cands.append((y, [r]))

            for pt in self.xre_dict:
                for x, rs in list(cands):
                    if not pt.search(x):
                        continue
                    for y, r in self.xre_dict[pt]:
                        cands.append((xre.sub(pt, y, x), rs + [r]))

            if len(cands) > 1:
                ys = [y for y, _ in cands]
                y, rs = random.choice(cands[1:])
                ls.append((w, y, rs, ys))
                out = out[:i + k] + y + out[j + k:]
                k += len(y) - (j - i)

        return line, out, ls

    def print(self, line, out, ls, op):

        if op == "all" \
        or op == "diff" and line != out \
        or op == "same" and line == out:
            print(out, end = "")

        if self.verbose:
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

if __name__ == "__main__":

    if len(sys.argv) not in (2, 3):
        sys.exit("Usage: %s all|diff|same [-v] < txt" % sys.argv[0])

    op = sys.argv[1]
    path = (os.path.dirname(__file__) or ".") + "/"
    tst = ko_chat_style_transfer(
        lex_dict = "",
        xre_dict = path + "ko_chat_style_transfer.xre",
        verbose = (len(sys.argv) == 3 and sys.argv[2] == "-v")
    )

    for line in sys.stdin:
        tst.print(*tst.transfer(line), op)

