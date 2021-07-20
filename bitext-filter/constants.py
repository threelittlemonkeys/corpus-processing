import re

MAX_SENT_LEN = 100
MIN_SENT_LEN = 1
MAX_WORD_LEN = 20
SENT_LEN_RATIO = 5

RE_ALPHA_L = re.compile("(?<=[A-Za-z\u00C0-\u00FF\u0400-\u04FF])(?=[^ A-Za-z\u00C0-\u00FF\u0400-\u04FF])")
RE_ALPHA_R = re.compile("(?<=[^ A-Za-z\u00C0-\u00FF\u0400-\u04FF])(?=[A-Za-z\u00C0-\u00FF\u0400-\u04FF])")
RE_NUM_L = re.compile("(?<=[0-9])(?=[^ 0-9])")
RE_NUM_R = re.compile("(?<=[^ 0-9])(?=[0-9])")
RE_NON_ALNUM_L = re.compile("(?<=[^ 0-9A-Za-z\u00C0-\u00FF\u0400-\u04FF])(?=[^ ])")
RE_NON_ALNUM_R = re.compile("(?<=[^ ])(?=[^ 0-9A-Za-z\u00C0-\u00FF\u0400-\u04FF])")

RE_PUNC = re.compile("[,.?!，．。？！]")
RE_BRACKET = re.compile("[<>(){}[\]「」『』《》【】]")
RE_QUOTATION = re.compile("(?<![a-z])[`'](?!(cause|em))|(?<!(in| o))[`'](?![a-z])|[\"“”]")
RE_URL = re.compile("https?://")
RE_REPETITION = re.compile("(.{3,})\\1{3,}")
RE_INVALID_WORD = re.compile("[a-z][a-z0-9]*[^ a-z0-9\u00C0-\u00FF\u0400-\u04FF\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7A3,.'/<>(){}[\]-]+[a-z0-9]")

RE_LANG_EN = re.compile("[a-z]")
RE_LANG_JA = re.compile("[\u3040-\u30FF]")
RE_LANG_KO = re.compile("[\uAC00-\uD7A3]")
RE_LANG_ZH = re.compile("[\u4E00-\u9FFF]")
RE_LANG_RU = re.compile("[\u0400-\u04FF]")
RE_LANG_CJK = re.compile("[\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7A3]")

RE_SENTS_EN = re.compile("([^ .?!]+( [^ .?!]+){12}[.?!]){2}")
RE_SENTS_KO = re.compile("([^.?!]{12}[\uAC00-\uD7A3][.?!]){2}")
RE_SENTS_ZH = re.compile("([^.?!]{12}[\uAC00-\uD7A3][.?!]){2}")

EN_NUMS = {
    "one": 1, "first": 1,
    "two": 2, "second": 2,
    "three": 3, "third": 3,
    "four": 4, "fourth": 4,
    "five": 5, "fifth": 5,
    "six": 6, "sixth": 6,
    "seven": 7, "seventh": 7,
    "eight": 8, "eighth": 8,
    "nine": 9, "ninth": 9,
    "ten": 10, "tenth": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
    "hundred": 100,
    "thousand": 1000,
    "million": 1000000,
    "billion": 1000000000,
    "trillion": 1000000000000,
}

ZH_NUMS = {
    "〇": 0, "零": 0,
    "一": 1, "壹": 1,
    "二": 2, "貳": 2, "两": 2,
    "三": 3, "叁": 3,
    "四": 4, "肆": 4,
    "五": 5, "伍": 5,
    "六": 6, "陸": 6,
    "七": 7, "柒": 7,
    "八": 8, "捌": 8,
    "九": 9, "玖": 9,
    "十": 10, "拾": 10,
    "百": 100, "佰": 100,
    "千": 1000, "仟": 1000,
    "万": 10000, "萬": 10000,
    "亿": 100000000, "億": 100000000,
    "兆": 1000000000000,
}
