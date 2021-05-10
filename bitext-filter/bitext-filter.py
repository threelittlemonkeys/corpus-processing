from utils import *

def corpus_filter(fn_raw, fn_tag):

    ln_err = 0
    ln_sum = 0
    timer = time.time()

    fo_raw = open(fn_raw)
    fo_tag = open(fn_tag) if fn_tag else None
    fa = open(fn_raw + ".flt.in", "w")
    fb = open(fn_raw + ".flt.out", "w")
    fc = open(fn_raw + ".flt.log", "w")

    for line_raw in fo_raw:
        error_log.clear()

        if line_raw.count("\t") != 2:
            exit(line_raw)
        idx, s0, t0 = line_raw.split("\t")
        s0 = s0.strip()
        t0 = t0.strip()
        s1 = normalize(s0)
        t1 = normalize(t0)

        if s1 == "":
            log_error("SRC_EMPTY")
        if t1 == "":
            log_error("TGT_EMPTY")
        if s1 == t1:
            log_error("SRC_AND_TGT_IDENTICAL")
        else:
            if s1 in t1:
                log_error("SRC_IN_TGT")
            if t1 in s1:
                log_error("TGT_IN_SRC")

        '''
        if not compare_findall(RE_BRACKET, s1, t1):
            log_error("BRACKET_MISMATCH")
        if not compare_findall(RE_QUOTATION, s1, t1):
            log_error("QUOTATION_MISMATCH")
        '''

        for txt, lang, side, in ((s1, SRC_LANG, "SRC"), (t1, TGT_LANG, "TGT")):

            if RE_URL.search(txt):
                log_error("URL_IN_%s" % side)
            if RE_REPETITION.match(txt):
                log_error("%s_REPEATED" % side)
            if RE_INVALID_WORD.search(txt):
                log_error("INVALID_WORD_IN_%s" % side)

            if lang == "en" and not RE_LANG_EN.search(txt) \
            or lang == "ko" and not RE_LANG_KO.search(txt) \
            or lang == "zh" and not RE_LANG_ZH.search(txt):
                log_error("INVALID_%s_LANGUAGE" % side)

            if lang == "en" and RE_LANG_CJK.search(txt) \
            or lang == "ja" and RE_LANG_KO.search(txt) \
            or lang == "ko" and (RE_LANG_JA.search(txt) or RE_LANG_ZH.search(txt)) \
            or lang == "zh" and (RE_LANG_KO.search(txt) or RE_LANG_JA.search(txt)):
                log_error("INVALID_LANGUAGE_IN_%s" % side)

            if lang == "en" and RE_SENTS_EN.search(txt) \
            or lang == "ko" and RE_SENTS_KO.search(txt) \
            or lang == "zh" and RE_SENTS_ZH.search(txt):
                log_error("MULTIPLE_SENTENCES_IN_%s" % side)

        s2 = tokenize(s1, SRC_LANG)
        t2 = tokenize(t1, TGT_LANG)

        if len(s2) > MAX_SENT_LEN:
            log_error("SRC_TOO_LONG")
        if len(t2) > MAX_SENT_LEN:
            log_error("TGT_TOO_LONG")
        if len(s2) < MIN_SENT_LEN:
            log_error("SRC_TOO_SHORT")
        if len(t2) < MIN_SENT_LEN:
            log_error("TGT_TOO_SHORT")

        if len(s2) / len(t2) > SENT_LEN_RATIO:
            log_error("SRC_TOO_LONGER")
        if len(t2) / len(s2) > SENT_LEN_RATIO:
            log_error("TGT_TOO_LONGER")
        if any(map(lambda x: len(x) > MAX_WORD_LEN, s2)):
            log_error("LONG_WORD_IN_SRC")
        if any(map(lambda x: len(x) > MAX_WORD_LEN, t2)):
            log_error("LONG_WORD_IN_TGT")

        if fo_tag:
            line_tag = fo_tag.readline()
            s3, t3 = line_tag.split("\t")
            s3 = s3.strip().split(" ")
            t3 = t3.strip().split(" ")
            s3 = [re.split("/(?=[^/]+$)", x) for x in s3]
            t3 = [re.split("/(?=[^/]+$)", x) for x in t3]

            s3_nnp = extract_nnp(s3, SRC_LANG)
            t3_nnp = extract_nnp(t3, TGT_LANG)
            if len(s3_nnp) or len(t3_nnp):
                print(s0)
                print(s3_nnp)
                print(t0)
                print(t3_nnp)
                input()
            if len(s3_nnp) and len(t3_nnp) and len(s3_nnp) != len(t3_nnp):
                log_error("NNP_MISMATCH")

        '''
        src_nums = word_to_number(src, SRC_LANG)
        tgt_nums = word_to_number(tgt, TGT_LANG)
        nums = src_nums.symmetric_difference(tgt_nums)
        if len(nums) > 1:
            log_error("NUMBER_MISMATCH")
        '''

        if error_log:
            for error_code in error_log:
                print(idx, s0, t0, error_code, sep = "\t", file = fb)
            ln_err += 1
        else:
            print(idx, s0, t0, sep = "\t", file = fa)
        ln_sum += 1
        if ln_sum % 100000 == 0:
            print("%d sentence pairs" % ln_sum)

    timer = time.time() - timer

    for code, cnt in sorted(error_cnt.items(), key = lambda x: -x[1]):
        print(code, cnt, "(%.4f%%)" % (cnt / ln_sum * 100), file = fc)
    print(file = fc)
    print("%d sentence pairs in total" % ln_sum, file = fc)
    print("%d sentence pairs filtered out (%.4f%%)" % (ln_err, ln_err / ln_sum * 100), file = fc)
    print("%f seconds" % timer, file = fc)

    fo_raw.close()
    fo_tag.close() if fo_tag else True
    fa.close()
    fb.close()
    fc.close()

if __name__ == "__main__":
    if len(sys.argv) not in (4, 5):
        sys.exit("Usage: %s src_lang tgt_lang raw tagged" % sys.argv[0])

    SRC_LANG = sys.argv[1]
    TGT_LANG = sys.argv[2]
    fn_raw = sys.argv[3]
    fn_tag = sys.argv[4] if len(sys.argv) == 5 else ""

    print("SRC_LANG = %s" % SRC_LANG)
    print("TGT_LANG = %s" % TGT_LANG)
    corpus_filter(fn_raw, fn_tag)
