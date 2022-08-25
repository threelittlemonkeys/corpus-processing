import sys
import re

EN = "a-z"
JA_HIRAGANA = "\u3041-\u3096\u3099-\u309C"
JA_KATAKANA = "\u30A1-\u30FA\u30FC"
JA_KANJI = "\u4E00-\u9FFF"
JA = JA_HIRAGANA + JA_KATAKANA + JA_KANJI
KO = "\uAC00-\uD7AF"

NUM = "0-9"

ALPHA = EN + JA + KO
ALNUM += NUM

RE_L = lambda char_set: re.compile("(?<=[^ %s])(?=[%s])" % ((char_set,) * 2))
RE_R = lambda char_set: re.compile("(?<=[%s])(?=[^ %s])" % ((char_set,) * 2))

RE_NON_ALNUM = re.compile("[^%s]+" % ALNUM)

RE_ALPHA_L = RE_L(ALNUM)
RE_ALPHA_R = RE_R(ALNUM)
RE_NUM_L = RE_L(NUM)
RE_NUM_R = RE_R(NUM)

RE_EN_L = RE_L(EN)
RE_EN_R = RE_R(EN)

RE_JA_KATAKANA_L = re.compile("(?<=[^ %s])(?=[%s])" % ((JA_KATAKANA,) * 2))
RE_JA_KATAKANA_R = re.compile("(?<=[%s])(?=[^ %s])" % ((JA_KATAKANA,) * 2))
RE_JA_KANJI_L = re.compile("(?<=[^ %sおご])(?=[%s])" % ((JA_KANJI,) * 2))
RE_JA_KANJI_ADP = re.compile("(?<=[%s])(?=[はがのを]\\b)" % JA_KANJI)

RE_LANG_JA = re.compile("[%s]" % JA)
RE_LANG_KO = re.compile("[%s]" % KO)

def tokenize(lang, txt, lc = True, alnum_only = False):

    if lc:
        txt = txt.lower()

    if alnum_only:
        txt = RE_NON_ALNUM.sub(" ", txt)

    txt = RE_ALPHA_L.sub(" ", txt)
    txt = RE_ALPHA_R.sub(" ", txt)
    txt = RE_NUM_L.sub(" ", txt)
    txt = RE_NUM_R.sub(" ", txt)

    if lang == "ja":
        txt = RE_EN_L.sub(" ", txt)
        txt = RE_EN_R.sub(" ", txt)
        txt = RE_JA_KATAKANA_L.sub(" ", txt)
        txt = RE_JA_KATAKANA_R.sub(" ", txt)
        txt = RE_JA_KANJI_L.sub(" ", txt)
        txt = RE_JA_KANJI_ADP.sub(" ", txt)

    txt = re.sub("\s{2,}", " ", txt)
    txt = txt.strip()
    txt = txt.split(" ")

    return txt
