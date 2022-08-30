import sys
import re

EN = "A-Za-z"
JA_HIRAGANA = "\u3041-\u3096\u3099-\u309C"
JA_KATAKANA = "\u30A1-\u30FA\u30FC"
JA_KANJI = "\u4E00-\u9FFF"
JA = JA_HIRAGANA + JA_KATAKANA + JA_KANJI
KO = "\uAC00-\uD7AF"
ZH = "\u4E00-\u9FFF"

NUM = "0-9"

ALPHA = EN
ALPHA += "\xC0-\xFF" # Latin-1 Supplement
ALPHA += "\u0100-\u017F" # Latin Extended-A
ALPHA += "\u0180-\u024F" # Latin Extended-B
ALPHA += "\u1E00-\u1EFF" # Latin Extended Additional
ALPHA += JA + KO + ZH
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

RE_KO_L = RE_L(KO)
RE_KO_R = RE_R(KO)

RE_ZH_B = RE_B(ZH)
RE_ZH_L = RE_L(ZH)
RE_ZH_R = RE_R(ZH)
