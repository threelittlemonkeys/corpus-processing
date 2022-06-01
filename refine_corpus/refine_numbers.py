import sys
import re
from constants import *

def augment_data(src, tgt, pts, i, out):
    if i >= len(pts):
        out.append((src, tgt))
    else:
        for pt in pts[i]:
            _src = src.replace("{NUM:%d}" % i, pt)
            _tgt = tgt.replace("{NUM:%d}" % i, pt)
            augment_data(_src, _tgt, pts, i + 1, out)

fo = open(sys.argv[1])

for ln, line in enumerate(fo, 1):
    *idx, src, tgt = line.strip().split("\t")

    # number patterns
    src_pts = [(m.start(), m.group()) for m in RE_NUM.finditer(src)]
    tgt_pts = [(m.start(), m.group()) for m in RE_NUM.finditer(tgt)]

    if len(src_pts) == 0 or len(tgt_pts) == 0:
        # print(line, end = "")
        continue

    src_idx, src_num = zip(*src_pts)
    tgt_idx, tgt_num = zip(*tgt_pts)

    # normalized forms
    _src_num = [re.sub("[^0-9]", "", x) for x in src_num]
    _tgt_num = [re.sub("[^0-9]", "", x) for x in tgt_num]

    ms = [] # matches
    st = [False for _ in tgt_num]
    for ai, a0, a1 in zip(src_idx, src_num, _src_num):
        for i, (bi, b0, b1) in enumerate(zip(tgt_idx, tgt_num, _tgt_num)):
            if st[i]:
                continue
            flag = False

            if a1 == b1:
                st[i] = True
                if a0 != b0 \
                or RE_NUM_BIG.match(a0) and RE_NUM_BIG.match(b0):
                    flag = True

            if a1 in ("19" + b1, "20" + b1):
                flag = True
            if b1 in ("19" + a1, "20" + a1):
                flag = True

            if flag:
                ms.append(((ai, a0, a1), (bi, b0, b1)))

    if not ms:
        # print(line, end = "")
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

        if a0 != b0 and len(a0) != len(b0):

            if a1 == b1:
                pts.append((max(a0, b0, key = len),))
                if RE_NUM_SEP.match(pts[-1][0]):
                    pts[-1] += pts[-1][0].replace(",", ""),
                a2 = b2 = "{NUM:%d}" % tag_idx
                tag_idx += 1

            if a1 != b1:
                pts.append((a0, b0))
                a2 = b2 = "{NUM:%d}" % tag_idx
                tag_idx += 1

        if len(a0) == len(b0):

            if a0 == b0:
                pts.append((a0,))
                if a0 != a1 and RE_NUM_ONLY.match(a0):
                    pts[-1] += a1,
                if RE_NUM_ONLY.match(a0):
                    num = "{num:,}".format(num = int(a1))
                    if num != a0 and num != a1:
                        pts[-1] += num,
                a2 = b2 = "{NUM:%d}" % tag_idx
                tag_idx += 1

            if a0 != b0:
                if a0.count(" ") and not b0.count(" "):
                    a2 = b0
                if b0.count(" ") and not a0.count(" "):
                    b2 = a0
                if not a0.count(" ") and not b0.count(" "):
                    pts.append((a0, b0))
                    a2 = b2 = "{NUM:%d}" % tag_idx
                    tag_idx += 1

        ai += src_k
        bi += tgt_k
        src_out = src_out[:ai] + a2 + src_out[ai + len(a0):]
        tgt_out = tgt_out[:bi] + b2 + tgt_out[bi + len(b0):]
        src_k += len(a2) - len(a0)
        tgt_k += len(b2) - len(b0)

    if src == src_out and tgt == tgt_out:
        # print(line, end = "")
        continue

    out = []
    augment_data(src_out, tgt_out, pts, 0, out)
    for src_out, tgt_out in out:
        print(*idx, src_out, tgt_out, sep = "\t")

    continue
    print("ms =", ms)
    print("pts =", pts)
    print("src =", src)
    print("tgt =", tgt)
    input()

fo.close()
