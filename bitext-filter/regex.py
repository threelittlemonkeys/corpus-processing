import re
from dict import *

RE_ALPHA_L = re.compile("(?<=[a-z])(?=[^ a-z])")
RE_ALPHA_R = re.compile("(?<=[^ a-z])(?=[a-z])")
RE_NUM_L = re.compile("(?<=[0-9])(?=[^ 0-9])")
RE_NUM_R = re.compile("(?<=[^ 0-9])(?=[0-9])")
RE_NON_ALNUM_L = re.compile("(?<=[^ 0-9a-z])(?=[^ ])")
RE_NON_ALNUM_R = re.compile("(?<=[^ ])(?=[^ 0-9a-z])")

RE_BRACKET = re.compile("[<>(){}[\]「」『』《》【】]")
RE_QUOTATION = re.compile("(?<![a-z])[`'](?!(cause|em))|(?<!(in| o))[`'](?![a-z])|[\"“”]")
RE_URL = re.compile("https?://")
RE_REPETITION = re.compile("(.{3,})\\1{3,}")
RE_INVALID_WORD = re.compile("[a-z][a-z0-9]*[^ a-z0-9\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7A3,.'/<>(){}[\]-]+[a-z0-9]")

RE_LANG_EN = re.compile("[a-z]")
RE_LANG_JA = re.compile("[\u3040-\u30FF]")
RE_LANG_KO = re.compile("[\uAC00-\uD7A3]")
RE_LANG_ZH = re.compile("[\u4E00-\u9FFF]")
RE_LANG_CJK = re.compile("[\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7A3]")

RE_SENTS_EN = re.compile("([^ .?!]+( [^ .?!]+){12}[.?!]){2}")
RE_SENTS_KO = re.compile("([^.?!]{12}[\uAC00-\uD7A3][.?!]){2}")
RE_SENTS_ZH = re.compile("([^.?!]{12}[\uAC00-\uD7A3][.?!]){2}")

RE_NNP_EN = re.compile("^[A-Za-z'-]+$")
RE_NNP_KO = re.compile("^[A-Za-z\uAC00-\uD7A3-]+$")
RE_NNP_ZH = re.compile("")

RE_NUM_EN = "([0-9]+|%s)" % ("|".join(EN_NUMS))
RE_NUM_ZH = "([0-9]+|[%s])" % "".join(ZH_NUMS)
RE_NUM_EN_A = re.compile("%s(( -)? %s)+" % (RE_NUM_EN, RE_NUM_EN))
RE_NUM_EN_B = re.compile("%s(_%s)*$" % (RE_NUM_EN, RE_NUM_EN))
RE_NUM_ZH_A = re.compile("%s( %s)+" % (RE_NUM_ZH, RE_NUM_ZH))
RE_NUM_ZH_B = re.compile("%s(_%s)*$" % (RE_NUM_ZH, RE_NUM_ZH))
