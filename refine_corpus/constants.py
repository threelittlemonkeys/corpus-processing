import re

RE_NUM = re.compile("[0-9]([^0-9\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]*[0-9])+")
RE_NUM_SEP = re.compile("[0-9]{,2}(,[0-9]{3})*$")
RE_NUM_BIG = re.compile("[0-9,]{4,}(?![년호年])")
RE_NUM_ONLY = re.compile("[0-9,]+$")

_SQ = "'`´‘’′" # single quotation marks
_DQ = "\"˝“”″" # double quotation marks
_FQ = "《》「」『』【】" # full-width quotation marks
_BR = "()[]<>{}" # brackets
_SYM = "→" # symbols
_PUNC = "~,.?!:;"
QUOT = _SQ + _DQ + _FQ # quotation marks

# contractions

CNTR_WORD = {
    y.replace("'", x) for x in _SQ for y in
    ("ma'am", "o'clock")
}

CNTR_L = {
    y.replace("'", x) for x in _SQ for y in
    ("'cause", "'em", "'til", "'till", "'un", "'uns")
}

CNTR_R = [
    y.replace("'", x) for x in _SQ for y in
    ("'d", "'em", "'ll", "'m", "'re", "'s", "'t", "'ve")
]
CNTR_R = re.compile("(%s)$" % "|".join(map(re.escape, CNTR_R)))

RE_ALNUM = re.compile("[0-9A-Za-z\uAC00-\uD7AF]")
RE_TOKEN = re.compile("[%s]+|[^ %s]+" % (_PUNC, _PUNC))

RE_FIND_BR = re.compile("[%s]" % re.escape(_BR))
RE_FIND_SYM = re.compile("[%s]" % re.escape(_SYM))
RE_FIND_PUNC = re.compile("[%s]" % re.escape(_PUNC))
RE_FIND_PUNC_EOS = re.compile("[%s]+[%s]*$" % (re.escape(_PUNC), re.escape(QUOT)))
RE_FIND_QUOT = re.compile("[%s]" % QUOT)
