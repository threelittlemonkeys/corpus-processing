import sys
import re
import time
import math
from dictionary import *
from parameters import *
from utils import *

error_log = list()
error_cnt = {code: 0 for code in ERROR_CODE}

RE_ALPHA_L = re.compile("(?<=[a-z])(?=[^ a-z])")
RE_ALPHA_R = re.compile("(?<=[^ a-z])(?=[a-z])")
RE_NUM_L = re.compile("(?<=[0-9])(?=[^ 0-9])")
RE_NUM_R = re.compile("(?<=[^ 0-9])(?=[0-9])")
RE_NON_ALNUM_L = re.compile("(?<=[^ 0-9a-z])(?=[^ ])")
RE_NON_ALNUM_R = re.compile("(?<=[^ ])(?=[^ 0-9a-z])")

RE_NUM_EN = "([0-9]+|%s)" % ("|".join(EN_NUMS))
RE_NUM_ZH = "([0-9]+|[%s])" % "".join(ZH_NUMS)
RE_NUM_EN_A = re.compile("%s(( -)? %s)+" % (RE_NUM_EN, RE_NUM_EN))
RE_NUM_EN_B = re.compile("%s(_%s)*$" % (RE_NUM_EN, RE_NUM_EN))
RE_NUM_ZH_A = re.compile("%s( %s)+" % (RE_NUM_ZH, RE_NUM_ZH))
RE_NUM_ZH_B = re.compile("%s(_%s)*$" % (RE_NUM_ZH, RE_NUM_ZH))

def log_error(code):
    error_log.append(code)
    error_cnt[code] += 1

def normalize(txt):
    txt = re.sub("\s+", " ", txt)
    txt = re.sub("(?<=[0-9]),(?=[0-9]{3})", "", txt)
    txt = txt.lower()
    txt = txt.strip()
    return txt

def subiter(ro, p1, p2, txt):
    for m in ro.finditer(txt):
        a = m.group()
        b = re.sub(p1, p2, a)
        txt = txt.replace(a, b, 1)
    return txt

def tokenize(txt, lang):
    txt = RE_ALPHA_L.sub(" ", txt)
    txt = RE_ALPHA_R.sub(" ", txt)
    txt = RE_NUM_L.sub(" ", txt)
    txt = RE_NUM_R.sub(" ", txt)
    txt = RE_NON_ALNUM_L.sub(" ", txt)
    txt = RE_NON_ALNUM_R.sub(" ", txt)

    '''
    if lang == "en":
        txt = subiter(RE_NUM_EN_A, "[ -]+", "_", txt)
    if lang in ("ja", "ko", "zh"):
        txt = subiter(RE_NUM_ZH_A, " ", "_", txt)
    '''

    txt = txt.split(" ")
    return txt

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
