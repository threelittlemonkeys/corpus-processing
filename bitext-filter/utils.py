import sys
import time
import math
from constants import *

ERR_CODES = [
    "SRC_EMPTY",
    "TGT_EMPTY",
    "SRC_AND_TGT_IDENTICAL",
    "SRC_IN_TGT",
    "TGT_IN_SRC",
    "PUNCTUATION_MARK_MISMATCH",
    "BRACKET_MISMATCH",
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
err_cnt = {code: 0 for code in ERR_CODES}

def log_error(code):
    err_log.append(code)
    err_cnt[code] += 1

def normalize(txt, lc = True, alnum = False):
    if lc:
        txt = txt.lower()
    if alnum:
       txt = RE_NON_ALNUM.sub(" ", txt)
    txt = re.sub("\s+", " ", txt)
    txt = txt.strip()
    return txt

def tokenize(txt):
    txt = RE_ALPHA_L.sub(" ", txt)
    txt = RE_ALPHA_R.sub(" ", txt)
    txt = RE_NUM_L.sub(" ", txt)
    txt = RE_NUM_R.sub(" ", txt)
    txt = RE_NON_ALNUM_L.sub(" ", txt)
    txt = RE_NON_ALNUM_R.sub(" ", txt)
    txt = txt.split(" ")
    return txt

def compare_findall(ro, a, b):
    return len(ro.findall(a)) == len(ro.findall(b))

def extract_nnp(txt):
    tkn = tokenize(normalize(txt, lc = False, alnum = True))
    func = lambda i, w: i and len(w) > 3 and RE_NNP.match(w)
    return [x[1].lower() for x in enumerate(tkn) if func(*x)]

def word_similarity(a, b):
    if a == b:
        return True
    a = re.sub("(.)\\1+", "\\1", a)
    b = re.sub("(.)\\1+", "\\1", b)
    a = re.sub("(?<=[aeiouhwy])[^aeiouhwy]+$", "", a)
    b = re.sub("(?<=[aeiouhwy])[^aeiouhwy]+$", "", b)
    a = re.sub("[aeiouhwy]", "", a)
    b = re.sub("[aeiouhwy]", "", b)
    if a == b:
        return True
    if a[:3] == b[:3]:
        return True
    if a[-3:] == b[-3:]:
        return True
    return False
