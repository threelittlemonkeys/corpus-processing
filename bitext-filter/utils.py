import sys
import time
import math
from parameters import *
from regex import *

ERROR_CODE = [
    "SRC_EMPTY",
    "TGT_EMPTY",
    "SRC_AND_TGT_IDENTICAL",
    "SRC_IN_TGT",
    "TGT_IN_SRC",
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
    "NNP_MISMATCH",
    "NUMBER_MISMATCH",
]

error_log = list()
error_cnt = {code: 0 for code in ERROR_CODE}

def log_error(code):
    error_log.append(code)
    error_cnt[code] += 1

def normalize(txt):
    txt = re.sub("\s+", " ", txt)
    txt = re.sub("(?<=[0-9]),(?=[0-9]{3})", "", txt)
    txt = txt.lower()
    txt = txt.strip()
    return txt

def tokenize(txt, lang):
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

def extract_nnp(seq, lang):
    nnp = []
    for idx, (word, tag) in enumerate(seq):
        if not (idx and "A" <= word[0] <= "Z" or tag == "NNP"):
            continue
        if lang == "en":
            if not RE_NNP_EN.search(word):
                continue
        if lang == "ko":
            if not RE_NNP_KO.search(word):
                continue
        nnp.append(word)
    return nnp

def word_to_number(txt, lang):
    ns = list()
    w2n = lambda x, y: [y[x] if x in y else x for x in x.split("_")]

    for w in txt:
        n = []
        if lang == "en" and RE_NUM_EN_B.match(w):
            n = w2n(w, EN_NUMS)
        if lang in ("ja", "ko", "zh") and RE_NUM_ZH_B.match(w):
            n = w2n(w, ZH_NUMS)
        ns.extend(n)

    return set("".join(map(str, ns))) - {"0", "1"}
