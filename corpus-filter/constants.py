import re

EN = "a-z"
ES = "áéíñóúü"
JA_HIRAGANA = "\u3040-\u309F"
JA_KATAKANA = "\u30A0-\u30FF"
JA = "\u3005" + JA_HIRAGANA + JA_KATAKANA
KO = "\u3130-\u318F\uAC00-\uD7A3"
RU = "\u0400-\u04FF"
VI = "àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ\u0300-\u0303\u0306\u0309\u0323"
ZH = "\u4E00-\u9FFF"

CJK_LANGS = ("ja", "ko", "zh")

ALPHA = EN + ES + JA + KO + RU + VI + ZH
ALNUM = "0-9" + ALPHA
PUNC = ",.?!，．。？！"

SQ = "'`´‘’′" # single quotation marks
DQ = "\"˝“”″«»" # double quotation marks
FQ = "《》「」『』【】" # full-width quotation marks
QUOT = SQ + DQ + FQ

RE_ALPHA_L = re.compile("(?<=[%s])(?=[^ %s])" % ((ALPHA,) * 2))
RE_ALPHA_R = re.compile("(?<=[^ %s])(?=[%s])" % ((ALPHA,) * 2))

RE_ALPHA_JA_KANJI = re.compile("(?<=[^ %s])(?=[%s])" % ((ZH,) * 2))
RE_ALPHA_JA_KATAKANA = re.compile("(?<=[^ %s])(?=[%s])" % ((JA_KATAKANA,) * 2))
RE_ALPHA_ZH = re.compile("(?<=[%s])(?=[%s])" % ((ZH,) * 2))
RE_NUM = re.compile("[1-9]{3,}")
RE_NUM_L = re.compile("(?<=[0-9])(?=[^ 0-9])")
RE_NUM_R = re.compile("(?<=[^ 0-9])(?=[0-9])")

RE_ALNUM = re.compile("[%s]" % ALNUM)
RE_NON_ALNUM = re.compile("[^%s]" % ALNUM)
RE_NON_ALNUM_L = re.compile("(?<=[^ %s])(?=[^ ])" % ALNUM)
RE_NON_ALNUM_R = re.compile("(?<=[^ ])(?=[^ %s])" % ALNUM)

RE_PUNC = re.compile("[,.?!¿¡，．。？！]")
RE_PUNC_EOS = re.compile("[,.?!¿¡，．。？！\"]+$")
RE_BR = re.compile("[<>(){}[\]]")
RE_LS = re.compile("^([0-9]\. |[❶-➓・])")
RE_SYM = re.compile("[#$%&*+=@^|¶♪\u2190-\u21FF\u25A0-\u26FF\u2700-\u27BF]")

RE_URL = re.compile("https?://")
RE_REPETITION = re.compile("(.{3,})\\1{2,}")

RE_LANG_EN = re.compile("[%s]" % EN)
RE_LANG_JA = re.compile("[%s]" % (JA + ZH))
RE_LANG_JA_KANA = re.compile("[%s]" % JA)
RE_LANG_KO = re.compile("[%s]" % KO)
RE_LANG_ZH = re.compile("[%s]" % ZH)
RE_LANG_RU = re.compile("[%s]" % RU)
RE_LANG_VI = re.compile("[%s]" % (EN + VI))
RE_LANG_CJK = re.compile("[%s]" % (JA + KO + ZH))

RE_TOKEN = re.compile("[%s]+|[^ %s]+" % (PUNC, PUNC))

RE_SENTS_EN = re.compile("([^ .?!]+( [^ .?!]+){12}[.?!]){2}")
RE_SENTS_KO = re.compile("([^.?!]{12}[%s][.?!]){2}" % KO)
RE_SENTS_ZH = re.compile("([^.?!]{12}[%s][.?!]){2}" % ZH)

CNTR_W = {
    w.replace("'", c) for c in SQ for w in
    ("ma'am", "o'clock")
    + ("'cause", "'em", "'til", "'till", "'un", "'uns")
}

CNTR_R = {
    w.replace("'", c) for c in SQ for w in
    ("'d", "'em", "'ll", "'m", "'re", "'s", "'t", "'ve")
}
