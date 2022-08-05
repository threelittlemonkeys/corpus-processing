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

LS_MISMATCH = 1
SYM_MISMATCH = 1
BR_MISMATCH = 1
PUNC_MISMATCH = 1
QUOT_MISMATCH = 1

ALPHA_MISMATCH = 1
NUM_MISMATCH = 1
DICT_MISMATCH = 1

import os

SCRIPT_PATH = (os.path.dirname(__file__) or ".") + "/"
ENT_DICT_PATH = SCRIPT_PATH + "ent_dict.%s%s.tsv" % (SRC_LANG, TGT_LANG)
