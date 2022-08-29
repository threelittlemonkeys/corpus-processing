SRC_LANG = "ko"
TGT_LANG = "zh"

MAX_SENT_LEN = 100 # long: 100, short : 15
MIN_SENT_LEN = 1
MAX_WORD_LEN = 20

if (SRC_LANG, TGT_LANG) == ("ja", "ko"):
    SENT_LEN_RATIO = 2
else:
    SENT_LEN_RATIO = 3

# mismatch parameters: minimum mismatches to be filtered out (0 if disabled)

LS_MISMATCH = 1 # 1
SYM_MISMATCH = 3 # 3
BR_MISMATCH = 3 # 3
PUNC_MISMATCH = 5 # 5
QUOT_MISMATCH = 5 # 5

ALPHA_MISMATCH = 0 # 0
NUM_MISMATCH = 3 # 3
DICT_MISMATCH = 0 # 0

import os

SCRIPT_PATH = (os.path.dirname(__file__) or ".") + "/"
DICT_PATH = SCRIPT_PATH + "dict.%s%s.tsv" % (SRC_LANG, TGT_LANG)
