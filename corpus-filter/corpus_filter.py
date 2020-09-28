from utils import *

def corpus_filter(filename):
    fo = open(filename)
    fa = open(filename + ".a", "w")
    fb = open(filename + ".b", "w")
    timer = time.time()
    ln_err = 0
    ln_sum = 0

    for line in fo:
        error_log.clear()

        _src, _tgt = line.split("\t")
        _src = _src.strip()
        _tgt = _tgt.strip()
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

        if SRC_LANG == "en" and not re.search("[a-z]", src):
            log_error("SRC_INVALID_LANGUAGE")
        if TGT_LANG == "ko" and not re.search("[\uAC00-\uD7A3]", tgt):
            log_error("TGT_INVALID_LANGUAGE")
        if TGT_LANG == "zh" and not re.search("[\u4E00-\u9FFF]", tgt):
            log_error("TGT_INVALID_LANGUAGE")

        '''
        if re.match(r"(.{3,})\1{3,}", src):
            log_error("SRC_REPEATED")
        if re.match(r"(.{3,})\1{3,}", tgt):
            log_error("TGT_REPEATED")

        src = tokenize(src, SRC_LANG)
        tgt = tokenize(tgt, TGT_LANG)

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
        '''

        '''
        src_nums = word_to_number(src, SRC_LANG)
        tgt_nums = word_to_number(tgt, TGT_LANG)
        nums = src_nums.symmetric_difference(tgt_nums)
        if len(nums) > 1:
            log_error("NUMBER_MISMATCH")
        '''

        if error_log:
            print(_src, _tgt, error_log[0], sep = "\t", file = fb)
            ln_err += 1
        else:
            print(_src, _tgt, sep = "\t", file = fa)
        ln_sum += 1
        if ln_sum % 100000 == 0:
            print("%d sentence pairs" % ln_sum)

    fo.close()
    fa.close()
    fb.close()
    timer = time.time() - timer

    print()
    for code, cnt in sorted(error_cnt.items(), key = lambda x: -x[1]):
        print(code, cnt, "(%.4f%%)" % (cnt / ln_sum * 100))
    print()
    print("%d sentence pairs in total" % ln_sum)
    print("%d sentence pairs filtered out (%.4f%%)" % (ln_err, ln_err / ln_sum * 100))
    print("%f seconds" % timer)

if __name__ == "__main__":
    if len(sys.argv) not in (2, 4):
        sys.exit("Usage: %s [src_lang] [tgt_lang] filename" % sys.argv[0])

    if len(sys.argv) == 4:
        SRC_LANG = sys.argv[1]
        TGT_LANG = sys.argv[2]

    print("SRC_LANG = %s" % SRC_LANG)
    print("TGT_LANG = %s" % TGT_LANG)
    corpus_filter(sys.argv[-1])
