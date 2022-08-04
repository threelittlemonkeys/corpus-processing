import sys
import re

EN = "a-z0-9"
JA_HIRAGANA = "\u3041-\u309C"
JA_KATAKANA = "\u30A1-\u30FA\u30FC"
JA_KANJI = "\u4E00-\u9FFF"
JA = JA_HIRAGANA + JA_KATAKANA + JA_KANJI
KO = "\uAC00-\uD7AF"
ALNUM = EN + JA + KO

RE_ALNUM_EN_L = re.compile("(?<=[%s])(?=[^ %s])" % ((EN,) * 2))
RE_ALNUM_EN_R = re.compile("(?<=[^ %s])(?=[%s])" % ((EN,) * 2))
RE_ALPHA_JA_KANJI = re.compile("(?<=[^ %s])(?=[%s])" % ((JA_KANJI,) * 2))
RE_ALPHA_JA_KATAKANA_L = re.compile("(?<=[^ %s])(?=[%s])" % ((JA_KATAKANA,) * 2))
RE_ALPHA_JA_KATAKANA_R = re.compile("(?<=[%s])(?=[^ %s])" % ((JA_KATAKANA,) * 2))
RE_ALNUM_L = re.compile("(?<=[^ %s])(?=[%s])" % ((ALNUM,) * 2))
RE_ALNUM_R = re.compile("(?<=[%s])(?=[^ %s])" % ((ALNUM,) * 2))

def tokenize(lang, sent):

    sent = sent.lower()

    if lang == "ja":
        sent = RE_ALNUM_EN_L.sub(" ", sent)
        sent = RE_ALNUM_EN_R.sub(" ", sent)
        sent = RE_ALPHA_JA_KANJI.sub(" ", sent)
        sent = RE_ALPHA_JA_KATAKANA_L.sub(" ", sent)
        sent = RE_ALPHA_JA_KATAKANA_R.sub(" ", sent)

    sent = RE_ALNUM_L.sub(" ", sent)
    sent = RE_ALNUM_R.sub(" ", sent)

    sent = re.sub("\s{2,}", " ", sent)
    sent = sent.strip()
    sent = sent.split(" ")

    return sent
