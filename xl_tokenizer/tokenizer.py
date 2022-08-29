import sys
import re
from constants import *

EN = "a-z"
JA_HIRAGANA = "\u3041-\u3096\u3099-\u309C"
JA_KATAKANA = "\u30A1-\u30FA\u30FC"
JA_KANJI = "\u4E00-\u9FFF"
JA = JA_HIRAGANA + JA_KATAKANA + JA_KANJI
KO = "\uAC00-\uD7AF"
ZH = "\u4E00-\u9FFF"

NUM = "0-9"

ALPHA = EN + JA + KO + ZH
ALNUM = ALPHA + NUM

RE_B = lambda x: re.compile("(?<=[%s])(?=[%s])" % (x, x))
RE_L = lambda x: re.compile("(?<=[^ %s])(?=[%s])" % (x, x))
RE_R = lambda x: re.compile("(?<=[%s])(?=[^ %s])" % (x, x))

RE_ALPHA_L = RE_L(ALPHA)
RE_ALPHA_R = RE_R(ALPHA)
RE_NUM_L = RE_L(NUM)
RE_NUM_R = RE_R(NUM)
RE_NON_ALNUM = re.compile("[^%s]+" % ALNUM)

RE_EN_L = RE_L(EN)
RE_EN_R = RE_R(EN)

RE_JA_KANJI_L = re.compile("(?<=[^ %sおご])(?=[%s])" % ((JA_KANJI,) * 2))
RE_JA_KATAKANA_L = RE_L(JA_KATAKANA)
RE_JA_KATAKANA_R = RE_R(JA_KATAKANA)

RE_ZH_B = RE_B(ZH)
RE_ZH_L = RE_L(ZH)
RE_ZH_R = RE_R(ZH)

tagger = {}

def import_tagger(lang):

    if lang == "ja":
        # pip install mecab-python3 unidic-lite
        import MeCab
        tagger[lang] = MeCab.Tagger

    if lang == "ko":
        # pip install python-mecab-ko
        import mecab
        tagger[lang] = mecab.MeCab()

def normalize(txt, lc = True, alnum_only = False):

    if lc:
        txt = txt.lower()

    if alnum_only:
       txt = RE_NON_ALNUM.sub(" ", txt)

    txt = re.sub("\s+", " ", txt)
    txt = txt.strip()

    return txt

def tokenize(lang, txt, lc = True, alnum_only = False):

    txt = normalize(txt, lc, alnum_only)

    txt = RE_ALPHA_L.sub(" ", txt)
    txt = RE_ALPHA_R.sub(" ", txt)
    txt = RE_NUM_L.sub(" ", txt)
    txt = RE_NUM_R.sub(" ", txt)

    if lang == "ja":
        txt = RE_EN_L.sub(" ", txt)
        txt = RE_EN_R.sub(" ", txt)
        txt = RE_JA_KANJI_L.sub(" ", txt)
        txt = RE_JA_KATAKANA_L.sub(" ", txt)
        txt = RE_JA_KATAKANA_R.sub(" ", txt)

    if lang == "zh":
        txt = RE_ZH_B.sub(" ", txt)
        txt = RE_ZH_L.sub(" ", txt)
        txt = RE_ZH_R.sub(" ", txt)

    txt = re.sub("\s{2,}", " ", txt)
    txt = txt.strip()
    txt = txt.split(" ")

    return txt
