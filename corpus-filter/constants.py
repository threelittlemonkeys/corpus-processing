import re

EN = "a-z"
ES = "áéíñóúü"
JA_HIRAGANA = "\u3040-\u309F"
JA_KATAKANA = "\u30A0-\u30FF"
JA = "\u3005" + JA_HIRAGANA + JA_KATAKANA
KO = "\u3130-\u318F\uAC00-\uD7A3"
RU = "\u0400-\u04FF"
VI = "àáâãèéêìíòóôõùúýăđĩũơư\u0300-\u0303\u0306\u0309\u0323" \
    + "".join([chr(0x1ea0 + i * 16 + j) for i in range(6) for j in range(1, 16, 2)][:-3])
ZH = "\u4E00-\u9FFF"

CJK_LANGS = ("ja", "ko", "zh")

ALPHA = EN + ES + JA + KO + RU + VI + ZH
ALNUM = "0-9" + ALPHA
PUNC = ",.?!¿¡，．。？！"

SQ = "'`´‘’′" # single quotation marks
DQ = "\"˝“”″«»" # double quotation marks
FQ = "《》「」『』【】" # full-width quotation marks
QUOT = SQ + DQ + FQ

RE_ALPHA_L = re.compile("(?<=[%s])(?=[^ %s])" % ((ALPHA, ) * 2))
RE_ALPHA_R = re.compile("(?<=[^ %s])(?=[%s])" % ((ALPHA, ) * 2))

RE_ALPHA_JA_KANJI = re.compile("(?<=[^ %s])(?=[%s])" % ((ZH, ) * 2))
RE_ALPHA_JA_KATAKANA = re.compile("(?<=[^ %s])(?=[%s])" % ((JA_KATAKANA, ) * 2))
RE_ALPHA_ZH = re.compile("(?<=[%s])(?=[%s])" % ((ZH, ) * 2))

RE_NUM = re.compile("[0-9]+")
# RE_NUM = re.compile("([#][0-9]+|[0-9]+[^%s()]{,2}[0-9]+|[0-9]+(?=[^ %s])|[0-9]{2,})" % ((ALNUM, ) * 2))
RE_NUM_L = re.compile("(?<=[0-9])(?=[^ 0-9])")
RE_NUM_R = re.compile("(?<=[^ 0-9])(?=[0-9])")

RE_ALNUM = re.compile("[%s]" % ALNUM)
RE_NON_ALNUM = re.compile("[^%s]" % ALNUM)
RE_NON_ALNUM_L = re.compile("(?<=[^ %s])(?=[^ ])" % ALNUM)
RE_NON_ALNUM_R = re.compile("(?<=[^ ])(?=[^ %s])" % ALNUM)

RE_INVALID_CHAR = re.compile("[\uFFFC\uFFFD]")
RE_REPETITION = re.compile("(.{3,})\\1{2,}")

RE_LANG_EN = re.compile("[%s]" % EN)
RE_LANG_JA = re.compile("[%s]" % (JA + ZH))
RE_LANG_JA_KANA = re.compile("[%s]" % JA)
RE_LANG_KO = re.compile("[%s]" % KO)
RE_LANG_ZH = re.compile("[%s]" % ZH)
RE_LANG_RU = re.compile("[%s]" % RU)
RE_LANG_VI = re.compile("[%s]" % (EN + VI))
RE_LANG_CJK = re.compile("[%s]" % (JA + KO + ZH))

RE_TOKEN = re.compile("[%s]+|[^ %s]+" % ((PUNC, ) * 2))

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

RE_PUNC = re.compile("[%s]" % PUNC)
RE_BR = re.compile("[<>(){}[\]]")
RE_LS = re.compile("^([0-9A-Za-z]\. |[-・])")
RE_URL = re.compile("https?://")
RE_SYM = re.compile("["
    + "#$%&*+=@^|¶♪¦©®°҂"
	+ "\u2100-\u214F" # Letterlike Symbols	
	+ "\u20A0-\u20CF" # Currency Symbols
	+ "\u2150-\u218F" # Number Forms
	+ "\u2190-\u21FF" # Arrows
	+ "\u2200-\u22FF" # Mathematical Operators
	+ "\u2300-\u23FF" # Miscellaneous Technical
    + "\u2400-\u243F" # Control Pictures
    + "\u2440-\u245F" # Optical Character Recognition
	+ "\u2460-\u24FF" # Enclosed Alphanumerics
	+ "\u2500-\u257F" # Box Drawing
	+ "\u2580-\u259F" # Block Elements
	+ "\u25A0-\u25FF" # Geometric Shapes
	+ "\u2600-\u26FF" # Miscellaneous Symbols
	+ "\u2700-\u27BF" # Dingbats
	+ "\u27C0-\u27EF" # Miscellaneous Mathematical Symbols-A
	+ "\u27F0-\u27FF" # Supplemental Arrows-A
	+ "\u2800-\u28FF" # Braille Patterns
	+ "\u2900-\u297F" # Supplemental Arrows-B
	+ "\u2980-\u29FF" # Miscellaneous Mathematical Symbols-B
	+ "\u2A00-\u2AFF" # Supplemental Mathematical Operators
	+ "\u2B00-\u2BFF" # Miscellaneous Symbols and Arrows
    + "\u3200-\u32FF" # Enclosed CJK Letters and Months
    + "\u3300-\u33FF" # CJK Compatibility
    + "\u4DC0-\u4DFF" # Yijing Hexagram Symbols
    + "\uFFE0-\uFFEE" # Halfwidth and Fullwidth Forms
	+ "\U0001F000-\U0001F02F" # Mahjong Tiles
	+ "\U0001F030-\U0001F09F" # Domino Tiles
	+ "\U0001F0A0-\U0001F0FF" # Playing Cards
    + "\U0001F100-\U0001F1FF" # Enclosed Alphanumeric Supplement
	+ "\U0001F300-\U0001F5FF" # Miscellaneous Symbols and Pictographs
	+ "\U0001F600-\U0001F64F" # Emoticons (Emoji)
	+ "\U0001F650-\U0001F67F" # Ornamental Dingbats
	+ "\U0001F680-\U0001F6FF" # Transport and Map Symbols
	+ "\U0001F700-\U0001F77F" # Alchemical Symbols
	+ "\U0001F780-\U0001F7FF" # Geometric Shapes Extended
	+ "\U0001F800-\U0001F8FF" # Supplemental Arrows-C
	+ "\U0001F900-\U0001F9FF" # Supplemental Symbols and Pictographs
	+ "\U0001FA00-\U0001FA6F" # Chess Symbols
	+ "\U0001FA70-\U0001FAFF" # Symbols and Pictographs Extended-A
	+ "\U0001FB00-\U0001FBFF" # Symbols for Legacy Computing
    + "]")
