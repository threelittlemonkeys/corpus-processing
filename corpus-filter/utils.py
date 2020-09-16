import sys
import re
import time
from dictionary import *
from parameters import *
from utils import *

error_log = list()
error_cnt = {code: 0 for code in ERROR_CODE}

def log_error(code):
    error_log.append(code)
    error_cnt[code] += 1

def normalize(txt):
    txt = txt.lower()
    return txt

def tokenize(txt, lang):
    txt = re.sub("(?<=[^ ])(?=[^ 0-9a-z])", r" ", txt)
    txt = re.sub("(?<=[^ 0-9a-z])(?=[^ ])", r" ", txt)
    txt = txt.split(" ")
    return txt

def extract_nums(txt, lang):
    if lang == "en":
        nums = EN_NUMS
    criterion = lambda x: x.isnumeric()
    return list(filter(criterion, txt))
