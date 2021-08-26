import re

RE_NUM = re.compile("[0-9０-９]([^0-9０-９\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]*[0-9０-９])+")
RE_NUM_SEP = re.compile("[0-9]{,2}(,[0-9]{3})*$")
RE_NUM_BIG = re.compile("[0-9,]{4,}(?![년호年])")
RE_NUM_ONLY = re.compile("[0-9,]+$")

SQ = "'`´‘’′" # single quotation marks
DQ = "\"˝“”″" # double quotation marks
FQ = "《》「」『』【】" # full-width quotation marks
BR = "()[]<>{}" # brackets
QUOT = SQ + DQ + FQ # quotation marks

CNTR = { # contractions
    y.replace("'", x) for x in SQ for y in
    ("d", "ll", "m", "re", "s", "t", "ve")
    + ("'cause", "'em", "'til", "'till", "'un", "'uns", "ma'am")
}

RE_KO = re.compile("[\uAC00-\uD7AF]")
RE_ALNUM = re.compile("[0-9A-Za-z\uAC00-\uD7AF]")

RE_TOKENIZE_A = re.compile("[,.?!]|[^ ,.?!]+")
RE_TOKENIZE_B = re.compile("[,.?!%s]|[^ ,.?!%s]+" % (QUOT, QUOT))

RE_FIND_BR = re.compile("[%s]" % re.escape(BR))
RE_FIND_QUOT = re.compile("[%s]" % QUOT)
