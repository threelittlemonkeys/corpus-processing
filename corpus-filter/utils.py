import sys
import time
import math
from constants import *
from parameters import *
from collections import defaultdict

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
    "NUMBER_MISMATCH",
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
    if lang == "ja":
        txt = re.sub(RE_ALPHA_JA_KANJI, " ", txt)
        txt = re.sub(RE_ALPHA_JA_KATAKANA, " ", txt)
    if lang == "zh":
        txt = re.sub(RE_ALPHA_ZH, " ", txt)
    txt = RE_NUM_L.sub(" ", txt)
    txt = RE_NUM_R.sub(" ", txt)
    txt = RE_NON_ALNUM_L.sub(" ", txt)
    txt = RE_NON_ALNUM_R.sub(" ", txt)
    txt = txt.split(" ")
    return txt

def findall_diff(obj, a, b):
    def _count(ro, x):
        y = defaultdict(int)
        for m in ro.finditer(x):
            y[m.group()] += 1
        return y
    if type(obj) == re.Pattern:
        func = lambda x: _count(obj, x)
    else:
        func = obj
    a = func(a)
    b = func(b)
    c = list()
    for x in (*a, *b):
        if x in a and x in b:
            c.extend([x] * abs(a[x] - b[x]))
        elif x in a:
            c.extend([x] * a[x])
        elif x in b:
            c.extend([x] * b[x])
    return c

def count_quotes(txt):
    quotes = defaultdict(int)
    i = 0
    for w in RE_TOKEN.findall(txt):
        for j, c in enumerate(w):
            if w in CNTR_W:
                break
            if c not in QUOT:
                continue
            if c not in SQ:
                quotes[c] += 1
                continue
            if 0 < j < len(w) - 1 and w[j:] in CNTR_R:
                continue
            if j == len(w) - 1 and re.search(".{2}(in|s).$", w):
                if not re.search("(^| )[%s]" % SQ, txt[:i]):
                    continue
            quotes[c] += 1
        i += len(w) + 1
    return quotes

def count_nums(txt):
    nums = defaultdict(int)
    for w in RE_NUM.findall(txt):
        w = RE_NON_ALNUM.sub("", w)
        nums[w] += 1
    return nums
