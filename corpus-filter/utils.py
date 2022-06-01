import sys
import time
import math
from constants import *
from parameters import *

ERR_CODES = [
    "SRC_EMPTY",
    "TGT_EMPTY",
    "SRC_AND_TGT_IDENTICAL",
    "SRC_IN_TGT",
    "TGT_IN_SRC",
    "LIST_MARKER_MISMATCH",
    "SYMBOL_MISMATCH",
    "BRACKET_MISMATCH",
    "PUNCTUATION_MARK_MISMATCH",
    "QUOTATION_MISMATCH",
    "URL_IN_SRC",
    "URL_IN_TGT",
    "SRC_REPEATED",
    "TGT_REPEATED",
    "INVALID_SRC_LANGUAGE",
    "INVALID_TGT_LANGUAGE",
    "INVALID_LANGUAGE_IN_SRC",
    "INVALID_LANGUAGE_IN_TGT",
    "MULTIPLE_SENTENCES_IN_SRC",
    "MULTIPLE_SENTENCES_IN_TGT",
    "SRC_TOO_LONG",
    "TGT_TOO_LONG",
    "SRC_TOO_SHORT",
    "TGT_TOO_SHORT",
    "SRC_TOO_LONGER",
    "TGT_TOO_LONGER",
    "LONG_WORD_IN_SRC",
    "LONG_WORD_IN_TGT",
    "ENTITY_MISMATCH",
    "NUMBER_MISMATCH",
]

err_log = list()
err_cnt = [
    set(),
    {code: 0 for code in ERR_CODES}
]

def log_error(ln, code):
    err_log.append(code)
    err_cnt[0].add(ln)
    err_cnt[1][code] += 1

def normalize(txt, lc = True, alnum = False):
    if lc:
        txt = txt.lower()
    if alnum:
       txt = RE_NON_ALNUM.sub(" ", txt)
    txt = re.sub("\s+", " ", txt)
    txt = txt.strip()
    return txt

def tokenize(lang, txt):
    txt = RE_ALPHA_L.sub(" ", txt)
    txt = RE_ALPHA_R.sub(" ", txt)
    if lang in ("ja", "zh"):
        txt = re.sub(RE_ALPHA_CJ, " ", txt)
    txt = RE_NUM_L.sub(" ", txt)
    txt = RE_NUM_R.sub(" ", txt)
    txt = RE_NON_ALNUM_L.sub(" ", txt)
    txt = RE_NON_ALNUM_R.sub(" ", txt)
    txt = txt.split(" ")
    return txt

def findall_diff(ro, a, b):
    def _count(x):
        x = ro.finditer(x)
        y = dict()
        for m in x:
            m = m.group()
            if m not in y:
                y[m] = 0
            y[m] += 1
        return y
    a = _count(a)
    b = _count(b)
    c = list()
    for x in set([*a, *b]):
        if x in a and x in b:
            c.extend([x] * abs(a[x] - b[x]))
        elif x in a:
            c.extend([x] * a[x])
        elif x in b:
            c.extend([x] * b[x])
    return c
