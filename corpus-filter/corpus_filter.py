import sys
import re
import time
from dictionary import *
from parameters import *

error_log = list()
error_counts = {code: 0 for code in ERROR_CODE}

def log_error(code):
    error_log.append(code)
    error_counts[code] += 1

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

def corpus_filter(src_lang, tgt_lang, filename):
    fo = open(filename)
    timer = time.time()
    ln_err = 0
    ln_sum = 0

    for line in fo:
        line = line.strip()
        error_log.clear()

        _src, _tgt = line.split("\t")
        src = normalize(_src)
        tgt = normalize(_tgt)

        if src == "":
            log_error("SRC_EMPTY")
        if tgt == "":
            log_error("TGT_EMPTY")
        if src == tgt:
            log_error("SRC_AND_TGT_IDENTICAL")
        elif src in tgt:
            log_error("SRC_IN_TGT")
        elif tgt in src:
            log_error("TGT_IN_SRC")

        if src_lang == "en" and not re.search("[a-z]", src):
            log_error("SRC_INVALID_LANGUAGE")
        if tgt_lang == "zh" and not re.search("[\u4E00-\u9FFF]", tgt):
            log_error("TGT_INVALID_LANGUAGE")

        if re.match(r"(.{3,})\1{3,}", src):
            log_error("SRC_REPEATED")
        if re.match(r"(.{3,})\1{3,}", tgt):
            log_error("TGT_REPEATED")

        src = tokenize(src, src_lang)
        tgt = tokenize(tgt, src_lang)

        if len(src) > MAX_SENT_LEN:
            log_error("SRC_TOO_LONG")
        if len(tgt) > MAX_SENT_LEN:
            log_error("TGT_TOO_LONG")
        if len(src) < MIN_SENT_LEN:
            log_error("SRC_TOO_SHORT")
        if len(tgt) < MIN_SENT_LEN:
            log_error("TGT_TOO_SHORT")

        if len(src) / len(tgt) > SENT_LEN_RATIO:
            log_error("SRC_TOO_LONGER")
        if len(tgt) / len(src) > SENT_LEN_RATIO:
            log_error("TGT_TOO_LONGER")

        if any(map(lambda x: len(x) > MAX_WORD_LEN, src)):
            log_error("LONG_WORD_IN_SRC")
        if any(map(lambda x: len(x) > MAX_WORD_LEN, tgt)):
            log_error("LONG_WORD_IN_TGT")

        src_nums = extract_nums(src, src_lang)
        tgt_nums = extract_nums(tgt, tgt_lang)
        if src_nums or tgt_nums:
            pass
            # print(src, tgt)
            # print(src_nums, tgt_nums)

        if len(error_log):
            print(_src, _tgt, ",".join(error_log), sep = "\t")
            ln_err += 1
        ln_sum += 1

    fo.close()
    timer = time.time() - timer

    print()
    for code, cnt in sorted(error_counts.items(), key = lambda x: -x[1]):
        print(code, cnt, "(%.4f%%)" % (cnt / ln_sum * 100))
    print("%d sentence pairs filtered out (%.4f%%)" % (ln_err, ln_err / ln_sum * 100))
    print("%d sentence pairs in total" % ln_sum)
    print("%f seconds" % timer)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: %s src_lang tgt_lang filename" % sys.argv[0])

    corpus_filter(*sys.argv[1:])
