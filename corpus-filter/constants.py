import re

_EN = "a-z"
_ES = "áéíñóúü"
_JA = "\u3005\u3040-\u30FF"
_KO = "\u3130-\u318F\uAC00-\uD7A3"
_RU = "\u0400-\u04FF"
_VI = "àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ\u0300-\u0303\u0306\u0309\u0323"
_ZH = "\u4E00-\u9FFF"

CJK_LANGS = ("ja", "ko", "zh")

_ALPHA = _EN + _ES + _JA + _KO + _RU + _VI + _ZH
_ALNUM = "0-9" + _ALPHA
_PUNC = ",.?!，．。？！"

RE_ALPHA_L = re.compile("(?<=[%s])(?=[^ %s])" % (_ALPHA, _ALPHA))
RE_ALPHA_R = re.compile("(?<=[^ %s])(?=[%s])" % (_ALPHA, _ALPHA))
RE_NUM_L = re.compile("(?<=[0-9])(?=[^ 0-9])")
RE_NUM_R = re.compile("(?<=[^ 0-9])(?=[0-9])")

RE_ALNUM = re.compile("[%s]" % _ALNUM)
RE_NON_ALNUM = re.compile("[^%s]" % _ALNUM)
RE_NON_ALNUM_L = re.compile("(?<=[^ %s])(?=[^ ])" % _ALNUM)
RE_NON_ALNUM_R = re.compile("(?<=[^ ])(?=[^ %s])" % _ALNUM)

RE_PUNC = re.compile("[,.?!，．。？！]")
RE_PUNC_EOS = re.compile("[,.?!，．。？！\"]+$")
RE_BRACKET = re.compile("[<>(){}[\]「」『』《》【】]")
RE_LIST_MARKER = re.compile("^([0-9]\. |[・])")
RE_QUOTATION = re.compile("(?<![a-z])[`'](?!(cause|em))|(?<!(in| o))[`'](?![a-z])|[\"“”]")
RE_SYMBOL = re.compile("[@#%*+=♪\u2190-\u21FF\u25A0-\u26FF\u2700-\u27BF]")

RE_URL = re.compile("https?://")
RE_REPETITION = re.compile("(.{3,})\\1{2,}")

RE_LANG_EN = re.compile("[%s]" % _EN)
RE_LANG_JA = re.compile("[%s]" % (_JA + _ZH))
RE_LANG_KO = re.compile("[%s]" % _KO)
RE_LANG_ZH = re.compile("[%s]" % _ZH)
RE_LANG_RU = re.compile("[%s]" % _RU)
RE_LANG_VI = re.compile("[%s]" % _EN + _VI)
RE_LANG_CJK = re.compile("[%s]" % (_JA + _KO + _ZH))

RE_SENTS_EN = re.compile("([^ .?!]+( [^ .?!]+){12}[.?!]){2}")
RE_SENTS_KO = re.compile("([^.?!]{12}[%s][.?!]){2}" % _KO)
RE_SENTS_ZH = re.compile("([^.?!]{12}[%s][.?!]){2}" % _ZH)
