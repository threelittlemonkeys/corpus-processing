import os

SRC_LANG = "ja"
TGT_LANG = "ko"

MAX_SENT_LEN = 100 # long: 100, short : 15
MIN_SENT_LEN = 1
MAX_WORD_LEN = 20

if (SRC_LANG, TGT_LANG) == ("ja", "ko"):
    SENT_LEN_RATIO = 2
else:
    SENT_LEN_RATIO = 3

# mismatch parameters: minimum mismatches to be filtered out (0 if disabled)

STRICT = False

LS_MISMATCH = 1 if STRICT else 1
SYM_MISMATCH = 1 if STRICT else 3
BR_MISMATCH = 1 if STRICT else 3
PUNC_MISMATCH = 1 if STRICT else 5
QUOT_MISMATCH = 1 if STRICT else 5

ALPHA_MISMATCH = 1 if STRICT else 0
NUM_MISMATCH = 1 if STRICT else 3
DICT_MISMATCH = 1 if STRICT else 0

SCRIPT_PATH = (os.path.dirname(__file__) or ".") + "/"
DICT_PATH = SCRIPT_PATH + "dict.%s%s.tsv" % (SRC_LANG, TGT_LANG)
