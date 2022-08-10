import sys
import re

EN = "a-z0-9"
JA_HIRAGANA = "\u3041-\u309C"
JA_KATAKANA = "\u30A1-\u30FA\u30FC"
JA_KANJI = "\u4E00-\u9FFF"
JA = JA_HIRAGANA + JA_KATAKANA + JA_KANJI
KO = "\uAC00-\uD7AF"
ALNUM = EN + JA + KO

RE_NON_ALNUM = re.compile("[^%s]" % ALNUM)

RE_EN_L = re.compile("(?<=[%s])(?=[^ %s])" % ((EN,) * 2))
RE_EN_R = re.compile("(?<=[^ %s])(?=[%s])" % ((EN,) * 2))

RE_JA_KATAKANA_L = re.compile("(?<=[^ %s])(?=[%s])" % ((JA_KATAKANA,) * 2))
RE_JA_KATAKANA_R = re.compile("(?<=[%s])(?=[^ %s])" % ((JA_KATAKANA,) * 2))
RE_JA_KANJI_L = re.compile("(?<=[^ %sおご])(?=[%s])" % ((JA_KANJI,) * 2))
RE_JA_KANJI_ADP = re.compile("(?<=[%s])(?=[はがのを]\\b)" % JA_KANJI)

RE_ALNUM_L = re.compile("(?<=[^ %s])(?=[%s])" % ((ALNUM,) * 2))
RE_ALNUM_R = re.compile("(?<=[%s])(?=[^ %s])" % ((ALNUM,) * 2))

RE_LANG_JA = re.compile("[%s]" % JA)
RE_LANG_KO = re.compile("[%s]" % KO)

def tokenize(lang, sent, alnum_only = False):

    sent = sent.lower()

    if alnum_only:
        sent = RE_NON_ALNUM.sub(" ", sent)

    sent = RE_ALNUM_L.sub(" ", sent)
    sent = RE_ALNUM_R.sub(" ", sent)

    if lang == "ja":
        sent = RE_EN_L.sub(" ", sent)
        sent = RE_EN_R.sub(" ", sent)
        sent = RE_JA_KATAKANA_L.sub(" ", sent)
        sent = RE_JA_KATAKANA_R.sub(" ", sent)
        sent = RE_JA_KANJI_L.sub(" ", sent)
        sent = RE_JA_KANJI_ADP.sub(" ", sent)

    sent = re.sub("\s{2,}", " ", sent)
    sent = sent.strip()
    sent = sent.split(" ")

    return sent
