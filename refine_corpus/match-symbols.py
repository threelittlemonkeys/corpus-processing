import os
import sys
import re

PATH = (os.path.dirname(__file__) or ".") + "/"

_SYM = list()
with open(PATH + "match-symbols.csv") as fo:
    for line in fo:
        c = line.split(" ")[1][0]
        _SYM.append(c)

_SYM = re.escape("".join(_SYM))
RE_SYM_L = re.compile("^[ %s]*" % _SYM, re.I)
RE_SYM_R = re.compile("[ %s]*$" % _SYM, re.I)

for line in sys.stdin:

    if line.count("\t") != 1:
        continue

    src, tgt = line.strip().split("\t")

    src_sym_l = RE_SYM_L.search(src).group()
    tgt_sym_l = RE_SYM_L.search(tgt).group()
    src_sym_r = RE_SYM_R.search(src).group()
    tgt_sym_r = RE_SYM_R.search(tgt).group()

    out = tgt

    if src_sym_l and src_sym_l != tgt_sym_l:
        out = src_sym_l + out[len(tgt_sym_l):]

    if src_sym_r and src_sym_r != tgt_sym_r:
        out = out[:len(out) - len(tgt_sym_r)] + src_sym_r

    print(src, out, sep = "\t")
