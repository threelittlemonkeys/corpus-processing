import sys
import re
from constants import *

if len(sys.argv) != 3:
    sys.exit("Usage: %s filename -[adv]" % sys.argv[0])

fo = open(sys.argv[1])
flag = sys.argv[2]
assert flag in ("-a", "-d", "-v")

def augment_data(src, tgt, pts, i, out):
    if i >= len(pts):
        out.append((src, tgt))
    else:
        for pt in pts[i]:
            _src = src.replace("{NUM:%d}" % i, pt)
            _tgt = tgt.replace("{NUM:%d}" % i, pt)
            augment_data(_src, _tgt, pts, i + 1, out)

for ln, line in enumerate(fo, 1):
    *idx, src, tgt = line.strip().split("\t")

    # number patterns
    src_pts = [(m.start(), m.group()) for m in RE_NUM.finditer(src)]
    tgt_pts = [(m.start(), m.group()) for m in RE_NUM.finditer(tgt)]

    if len(src_pts) == 0 or len(tgt_pts) == 0:
        if flag == "-a":
            print(line, end = "")
        continue

    src_idxs, src_nums = zip(*src_pts)
    tgt_idxs, tgt_nums = zip(*tgt_pts)

    # normalized forms
    _src_nums = [re.sub("[^0-9]", "", x) for x in src_nums]
    _tgt_nums = [re.sub("[^0-9]", "", x) for x in tgt_nums]

    ms = [] # matches
    st = [False for _ in tgt_nums]
    for ai, a0, a1 in zip(src_idxs, src_nums, _src_nums):
        for i, (bi, b0, b1) in enumerate(zip(tgt_idxs, tgt_nums, _tgt_nums)):
            if st[i]:
                continue
            k = False

            if a1 == b1:
                k = True
            '''
            # year
            if a1 in ("19" + b1, "20" + b1):
                k = True
            if b1 in ("19" + a1, "20" + a1):
                k = True
            '''
            if k:
                ms.append(((ai, a0, a1), (bi, b0, b1)))

    if not ms:
        if flag == "-a":
            print(line, end = "")
        continue

    pts = [] # patterns for data augmentation
    src_k = 0
    tgt_k = 0
    tag_idx = 0
    src_out = src
    tgt_out = tgt

    for m in ms:
        (ai, a0, a1), (bi, b0, b1) = m
        a2 = ""
        b2 = ""
        k = True

        if a0 == b0:

            if RE_NUM_SEP.match(a0):
                pts.append((a0, a0.replace(",", "")))
                k = False

        if a0 != b0:

            n0, n1 = sorted([a0, b0], key = len)

            if RE_NUM_ONLY.match(n0) and RE_NUM_SEP.match(n1):
                pts.append((n0, n1))
                k = False

        if k:
            continue

        a2 = b2 = "{NUM:%d}" % tag_idx
        tag_idx += 1

        ai += src_k
        bi += tgt_k
        src_out = src_out[:ai] + a2 + src_out[ai + len(a0):]
        tgt_out = tgt_out[:bi] + b2 + tgt_out[bi + len(b0):]
        src_k += len(a2) - len(a0)
        tgt_k += len(b2) - len(b0)

    if src == src_out and tgt == tgt_out:
        if flag == "-a":
            print(line, end = "")
        continue

    out = []
    augment_data(src_out, tgt_out, pts, 0, out)

    if flag == "-v":
        print("src =", src)
        print("tgt =", tgt)
        print("ms =", ms)
        print("pts =", pts)

    for src_out, tgt_out in out:
        print(*idx, src_out, tgt_out, sep = "\t")

    if flag == "-v":
        input()

fo.close()
