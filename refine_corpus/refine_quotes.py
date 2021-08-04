import sys
import re
import time
from utils import *

SQ = "'`´‘’′" # single quotation marks
DQ = "\"˝“”″" # double quotation marks
FQ = "《》「」『』【】" # full-width quotation marks
BR = "()[]<>{}" # brackets
QUOT = SQ + DQ + FQ # quotation marks

APOS_WORD = {
    y.replace("'", x) for x in SQ for y in
    ("'cause", "'em", "'til", "'till", "'un", "'uns", "ma'am")
}
APOS_PRT = {"d", "ll", "m", "re", "s", "t", "ve"}

RE_KO = re.compile("[\uAC00-\uD7AF]")
RE_ALNUM = re.compile("[0-9A-Za-z\uAC00-\uD7AF]")
RE_TOKENIZE_A = re.compile("[,.?!]|[^ ,.?!]+")
RE_TOKENIZE_B = re.compile("[,.?!%s]|[^ ,.?!%s]+" % (QUOT, QUOT))
RE_FIND_QUOT = re.compile("[%s]" % QUOT)
RE_FIND_BR = re.compile("[%s]" % re.escape(BR))

PRINT_FLAG = False

def _print(*args, **kwargs):
    if PRINT_FLAG:
        print(*args, **kwargs)

def any_alnum(txt):
    return RE_ALNUM.search(txt)

def find_quot(txt, seo = False):
    quot = list()

    for w in RE_TOKENIZE_A.finditer(txt):
        i, j = w.start(), w.end()
        w = w.group().lower()
        for m in RE_FIND_QUOT.finditer(w):
            k = m.start()
            m = m.group()

            # double quote
            if m in DQ:
                quot.append((i + k, m))
                continue

            # single quote
            if w in APOS_WORD:
                continue
            if w[k + 1:] in APOS_PRT:
                continue
            if k == 1 and w[0] in ("d" , "o"):
                continue
            if k == len(w) - 1 and (w[-2:-1] == "s" or w[-3:-1] == "in"):
                if not re.search("(^| )[%s]" % SQ, txt[:i]):
                    continue
                elif re.search("[%s]( |$)" % SQ, txt[j:]):
                    continue
            quot.append((i + k, m))

    if seo: # at sentence ends only
        for x in quot:
            if any_alnum(txt[:x[0]]) and any_alnum(txt[x[0] + 1:]):
                return

    return quot

def find_quoted_strings(txt, quot, qlen):
    if len(quot) != 2:
        return
    i, j = quot[0][0], quot[1][0]
    if i > 0 and RE_ALNUM.search(txt[i - 1]):
        return
    qstr = txt[i + 1:j].strip()
    if not qstr:
        return
    if qstr.count(" ") > qlen - 1:
        return
    return (i, qstr)

def find_transliteration(x, y):
    if RE_KO.search(x):
        x = romanize(x)
    if RE_KO.search(y):
        y = romanize(y)
    x = [w.group() for w in RE_TOKENIZE_B.finditer(x.lower())]
    y = y.lower()
    xs = []
    for z in (1, 2):
        for i in range(len(x) - z + 1):
            w = "".join(x[i:i + z])
            if RE_ALNUM.search(w):
                xs.append((w, edit_distance(w, y)))
    return min(xs, key = lambda x: x[1])

timer = time.time()
fo = open(sys.argv[1])

for ln, line in enumerate(fo, 1):
    idx, src, tgt = line.strip().split("\t")

    if ln % 100000 == 0:
        print("%d sentece pairs" % ln, file = sys.stderr)

    src_quot = find_quot(src)
    tgt_quot = find_quot(tgt)
    num_src_quot = len(src_quot)
    num_tgt_quot = len(tgt_quot)
    num_src_br = len(RE_FIND_BR.findall(src))
    num_tgt_br = len(RE_FIND_BR.findall(tgt))

    # Case 0

    if num_src_quot == num_tgt_quot and num_src_br == num_tgt_br == 0:
        _print(idx, src, tgt, sep = "\t")
        continue

    # Case 1: bracket mismatch

    if not num_src_br == num_tgt_br:
        _print(idx, src, tgt, sep = "\t")
        continue

    # Case 2: quotation marks only at sentence ends

    if (not num_src_quot or find_quot(src, seo = True)) and find_quot(tgt, seo = True):
        _print(idx, src, tgt, sep = "\t")
        continue

    if (not num_tgt_quot or find_quot(tgt, seo = True)) and find_quot(src, seo = True):
        _print(idx, src, tgt, sep = "\t")
        continue

    # Case 3: only one quoted string in the sentence
    # find transliterated target phrase

    src_qstr = find_quoted_strings(src, src_quot, qlen = 2)
    tgt_qstr = find_quoted_strings(tgt, tgt_quot, qlen = 2)

    if (not num_src_quot or find_quot(src, seo = True)) and tgt_qstr:
        tr = find_transliteration(src, tgt_qstr[1])
        if tr[1] <= 3:
            _print(src, tgt, sep = "\t")
            continue

    if (not num_tgt_quot or find_quot(tgt, seo = True)) and src_qstr:
        tr = find_transliteration(tgt, src_qstr[1])
        if tr[1] <= 3:
            _print(src, tgt, sep = "\t")
            continue

    if num_src_br != num_tgt_br:
        _print(idx, src, tgt, sep = "\t")
        continue

    # Case 4: leftovers
    # sentence segmentation
    # quote extraction
    # MT source selection from HT text
    # calculate HT-MT simliarity

    _print(src, tgt, sep = "\t")
    continue

fo.close()
timer = time.time() - timer

print("%f seconds" % timer, file = sys.stderr)
