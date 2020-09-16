import sys
import re
import time
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

_RE_NUM_EN = "(%s)" % "|".join(EN_NUMS)
_RE_NUM_ZH = "[%s]" % "".join(ZH_NUMS)
RE_NUM_EN_A = re.compile("%s(( -)? %s)+" % (_RE_NUM_EN, _RE_NUM_EN))
RE_NUM_EN_B = re.compile("%s(_%s)*$" % (_RE_NUM_EN, _RE_NUM_EN))
RE_NUM_ZH_A = re.compile("%s( %s)+" % (_RE_NUM_ZH, _RE_NUM_ZH))
RE_NUM_ZH_B = re.compile("%s(_%s)*$" % (_RE_NUM_ZH, _RE_NUM_ZH))

def log_error(code):
    error_log.append(code)
    error_cnt[code] += 1

def normalize(txt):
    txt = re.sub("\s+", " ", txt)
    txt = re.sub("(?<=[0-9])[ ,.]+(?=[0-9])", "", txt)
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

    if lang == "en":
        txt = subiter(RE_NUM_EN_A, "[ -]+", "_", txt)
    if lang == "zh":
        txt = subiter(RE_NUM_ZH_A, " ", "_", txt)

    txt = txt.split(" ")
    return txt

def word_to_number(word, lang):
    num = []

    if lang == "en":
        w2n = EN_NUMS
        units = ("hundred", "thousand", "million", "billion", "trillion")
    if lang == "zh":
        w2n = ZH_NUMS
        units = ("十", "百", "千", "万", "亿", "兆")

    for w in word.split("_"):
        if num and w in units:
            num[-1] *= w2n[w]
        else:
            num.append(w2n[w])
    return sum(num)

def extract_numbers(txt, lang):
    nums = list()

    for w in txt:
        if w.isdigit():
            n = int(w)
        elif lang == "en" and RE_NUM_EN_B.match(w):
            n = word_to_number(w, lang)
        elif lang == "zh" and RE_NUM_ZH_B.match(w):
            n = word_to_number(w, lang)
        else:
            continue
        nums.append(n)

    return nums
