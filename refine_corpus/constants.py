import re

RE_NUM = re.compile("[0-9]([^0-9\u0400-\u04FF\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7AF]?[0-9])+")
RE_NUM_SEP = re.compile("^[0-9]{,2}([, ][0-9]{3})+$")
RE_NUM_ONLY = re.compile("^[0-9]+$")

SQ = "'`´‘’′" # single quotation marks
DQ = "\"˝“”″«»" # double quotation marks
FQ = "《》「」『』【】" # full-width quotation marks
PUNC = "~,.?!:;"
QUOT = SQ + DQ + FQ # quotation marks

# contractions

CTR_WORD = {
    y.replace("'", x) for x in SQ for y in
    ("ma'am", "o'clock")
}

CTR_L = {
    y.replace("'", x) for x in SQ for y in
    ("'cause", "'em", "'til", "'till", "'un", "'uns")
}

CTR_R = [
    y.replace("'", x) for x in SQ for y in
    ("'d", "'em", "'ll", "'m", "'re", "'s", "'t", "'ve")
]
CTR_R = re.compile("(%s)$" % "|".join(map(re.escape, CTR_R)))

RE_ALNUM = re.compile("[0-9A-Za-z\uAC00-\uD7AF]")
RE_TOKEN = re.compile("[%s]+|[^ %s]+" % (PUNC, PUNC))

RE_PQ_EOS = re.compile("[ %s%s]+$" % (re.escape(PUNC), re.escape(QUOT)))
RE_QUOT = re.compile("[%s]" % QUOT)
