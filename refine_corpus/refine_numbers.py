import sys
import re
from clean_corpus import clean_text
from constants import *

def augment_data(src, tgt, pts, i, out):
    if i >= len(pts):
        out.append((src, tgt))
    else:
        for pt in pts[i]:
            _src = src.replace("{{NUM:%d}}" % i, pt)
            _tgt = tgt.replace("{{NUM:%d}}" % i, pt)
            augment_data(_src, _tgt, pts, i + 1, out)

fo = open(sys.argv[1])

for ln, raw in enumerate(fo):

    if raw.count("\t") != 2:
        # print(raw, end = "")
        continue
    idx, src, tgt = raw.strip().split("\t")

    # number patterns
    src_pt = [(m.start(), m.group()) for m in RE_NUM.finditer(src)]
    tgt_pt = [(m.start(), m.group()) for m in RE_NUM.finditer(tgt)]

    if len(src_pt) == 0 or len(tgt_pt) == 0:
        # print(raw, end = "")
        continue

    src_idx, src_num = zip(*src_pt)
    tgt_idx, tgt_num = zip(*tgt_pt)

    # normalized forms
    src_num_1 = [clean_text(x) for x in src_num]
    tgt_num_1 = [clean_text(x) for x in tgt_num]
    src_num_2 = [re.sub("[^0-9]", "", x) for x in src_num_1]
    tgt_num_2 = [re.sub("[^0-9]", "", x) for x in tgt_num_1]

    ms = [] # matches
    state = [False for _ in tgt_num]
    for ai, a0, a1, a2 in zip(src_idx, src_num, src_num_1, src_num_2):
        for i, (bi, b0, b1, b2) in enumerate(zip(tgt_idx, tgt_num, tgt_num_1, tgt_num_2)):
            if state[i]:
                continue
            flag = False

            if a2 == b2:
                state[i] = True
                if a1 != b1 \
                or (RE_NUM_BIG.match(src[ai:]) and RE_NUM_BIG.match(tgt[bi:]) \
                and not 1900 <= int(a2) <= 2020 and not 1900 <= int(b2) <= 2020):
                    flag = True

            if a1 in ("19" + b1, "20" + b1):
                flag = True

            if b1 in ("19" + a1, "20" + a1):
                flag = True

            if flag:
                ms.append(((ai, a0, a1, a2), (bi, b0, b1, b2)))
                state[i] = True
                break

    if not ms:
        # print(raw, end = "")
        continue

    pts = [] # patterns for data augmentation
    slot_idx = 0
    src_out = src
    tgt_out = tgt
    src_k = 0
    tgt_k = 0

    for m in ms:
        (ai, a0, a1, a2), (bi, b0, b1, b2) = m
        a3 = ""
        b3 = ""

        if a1 != b1 and len(a1) != len(b1):

            if a2 == b2:
                pts.append((max(a1, b1, key = len),))
                if RE_NUM_SEP.match(pts[-1][0]):
                    pts[-1] += pts[-1][0].replace(",", ""),
                a3 = b3 = "{{NUM:%d}}" % slot_idx
                slot_idx += 1

            if a2 != b2:
                pts.append((a1, b1))
                a3 = b3 = "{{NUM:%d}}" % slot_idx
                slot_idx += 1

        if len(a1) == len(b1):

            if a1 == b1:
                pts.append((a1,))
                if a1 != a2 and RE_NUM_ONLY.match(a1):
                    pts[-1] += a2,
                if RE_NUM_ONLY.match(a1):
                    num = "{num:,}".format(num = int(a2))
                    if num != a1 and num != a2:
                        pts[-1] += num,
                a3 = b3 = "{{NUM:%d}}" % slot_idx
                slot_idx += 1

            if a1 != b1:
                if a1.count(" ") and not b1.count(" "):
                    a3 = b1
                if b1.count(" ") and not a1.count(" "):
                    b3 = a1
                if not a1.count(" ") and not b1.count(" "):
                    pts.append((a1, b1))
                    a3 = b3 = "{{NUM:%d}}" % slot_idx
                    slot_idx += 1

        ai += src_k
        bi += tgt_k
        src_out = src_out[:ai] + a3 + src_out[ai + len(a0):]
        tgt_out = tgt_out[:bi] + b3 + tgt_out[bi + len(b0):]
        src_k += len(a3) - len(a0)
        tgt_k += len(b3) - len(b0)

    if src == src_out and tgt == tgt_out:
        # print(raw, end = "")
        continue

    out = []
    augment_data(src_out, tgt_out, pts, 0, out)
    for src_out, tgt_out in out:
        print(idx, src_out, tgt_out, sep = "\t")

    continue
    print(ms)
    print(pts)
    print(src)
    print(tgt)
    input()

fo.close()
