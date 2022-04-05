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
    "INVALID_WORD_IN_SRC",
    "INVALID_WORD_IN_TGT",
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
    txt = RE_NUM_L.sub(" ", txt)
    txt = RE_NUM_R.sub(" ", txt)
    txt = RE_NON_ALNUM_L.sub(" ", txt)
    txt = RE_NON_ALNUM_R.sub(" ", txt)
    txt = txt.split(" ")
    return txt

def diff_findall(ro, a, b):
    return abs(len(ro.findall(a)) - len(ro.findall(b)))
