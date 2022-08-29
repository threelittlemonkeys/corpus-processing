import os
import sys
import time
import math
from constants import *
from parameters import *
from collections import defaultdict

class logger():

    error_codes = [
        "SRC_EMPTY",
        "TGT_EMPTY",
        "SRC_AND_TGT_IDENTICAL",
        "SRC_IN_TGT",
        "TGT_IN_SRC",
        "LIST_MARKER_MISMATCH",
        "SYMBOL_MISMATCH",
        "BRACKET_MISMATCH",
        "PUNCTUATION_MARK_MISMATCH",
        "QUOTATION_MISMATCH",
        "ALPHABET_MISMATCH",
        "NUMBER_MISMATCH",
        "DICTIONARY_MISMATCH",
        "URL_IN_SRC",
        "URL_IN_TGT",
        "INVALID_CHARACTER_IN_SRC",
        "INVALID_CHARACTER_IN_TGT",
        "REPETITION_IN_SRC",
        "REPETITION_IN_TGT",
        "INVALID_SRC_LANGUAGE",
        "INVALID_TGT_LANGUAGE",
        "INVALID_LANGUAGE_IN_SRC",
        "INVALID_LANGUAGE_IN_TGT",
        "MULTIPLE_SENTENCES_IN_SRC",
        "MULTIPLE_SENTENCES_IN_TGT",
        "SRC_TOO_LONG",
        "TGT_TOO_LONG",
        "SRC_TOO_SHORT",
        "TGT_TOO_SHORT",
        "SRC_TOO_LONGER",
        "TGT_TOO_LONGER",
        "LONG_WORD_IN_SRC",
        "LONG_WORD_IN_TGT",
    ]

    def __init__(self):
        self.cats = {x: 0 for x in self.error_codes}
        self.lines = set()
        self.errors = []

    def log(self, ln, code):
        self.cats[code] += 1
        self.lines.add(ln)
        self.errors.append(code)

def print_parameters(stream):
    print("SRC_LANG =", SRC_LANG, file = stream)
    print("TGT_LANG =", TGT_LANG, file = stream)
    print("MAX_SENT_LEN =", MAX_SENT_LEN, file = stream)
    print("MIN_SENT_LEN =", MIN_SENT_LEN, file = stream)
    print("MAX_WORD_LEN =", MAX_WORD_LEN, file = stream)
    print("SENT_LEN_RATIO =", SENT_LEN_RATIO, file = stream)
    print("LS_MISMATCH =", LS_MISMATCH, file = stream)
    print("SYM_MISMATCH =", SYM_MISMATCH, file = stream)
    print("BR_MISMATCH =", BR_MISMATCH, file = stream)
    print("PUNC_MISMATCH =", PUNC_MISMATCH, file = stream)
    print("QUOT_MISMATCH =", QUOT_MISMATCH, file = stream)
    print("ALPHABET_MISMATCH =", ALPHA_MISMATCH, file = stream)
    print("NUMBER_MISMATCH =", NUM_MISMATCH, file = stream)
    print("DICT_MISMATCH =", DICT_MISMATCH, file = stream)

def findall_diff(obj, a, b):

    def _count(ro, x):
        y = defaultdict(int)
        for m in ro.finditer(x):
            y[m.group()] += 1
        return y

    if type(obj) == re.Pattern:
        func = lambda x: _count(obj, x)
    else:
        func = obj

    a = func(a)
    b = func(b)
    c = []

    for x in (a, b):
        if "¡" in x and "!" in x:
            x["¡"] -= x["!"]
        if "¿" in x and "?" in x:
            x["¿"] -= x["?"]

    for x in {*a, *b}:
        if x in a and x in b:
            c.extend([x] * abs(a[x] - b[x]))
        elif x in a:
            c.extend([x] * a[x])
        elif x in b:
            c.extend([x] * b[x])

    return c

def count_quotes(txt):
    quotes = defaultdict(int)
    i = 0
    for w in RE_TOKEN.findall(txt):
        for j, c in enumerate(w):
            if w in CNTR_W:
                break
            if c not in QUOT:
                continue
            if c not in SQ:
                quotes[c] += 1
                continue
            if 0 < j < len(w) - 1 and w[j:] in CNTR_R:
                continue
            if j == len(w) - 1 and re.search(".{2}(in|s).$", w):
                if not re.search("(^| )[%s]" % SQ, txt[:i]):
                    continue
            quotes[c] += 1
        i += len(w) + 1
    return quotes

def count_nums(txt):
    nums = defaultdict(int)
    for m in RE_NUM.finditer(txt):
        num = m.group()
        nums[num] += 1
    return nums

def load_dict(filename):
    if not os.path.isfile(filename):
        return {}, 0
    do = {}
    print("loading dictionary (%s)" % filename, file = sys.stderr)
    with open(filename) as fo:
        for line in fo:
            line = line.strip()
            if line == "":
                break
            x, y = line.split("\t")
            if x not in do:
                do[x] = []
            do[x].append(y)
    for x, ys in do.items():
        do[x] = re.compile("|".join(sorted(map(re.escape, ys), key = len)[::-1]))
    return (do, len(max(do, key = len)))

def match_dict(do, x, y):
    i = 0
    do, maxlen = do
    ls = [[], []]
    while i < len(x):
        for j in range(min(len(x), i + maxlen), i, -1):
            xw = x[i:j]
            if xw in do:
                i += len(xw)
                m = do[xw].search(y)
                yw = m.group() if m else None
                ls[0 if m else 1].append((xw, yw))
        else:
            i += 1
    return ls
