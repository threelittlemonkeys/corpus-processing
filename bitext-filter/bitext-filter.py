from utils import *
from lexicon import lexicon 

def corpus_filter(src_lang, tgt_lang, filename):

    print("src_lang = %s" % src_lang)
    print("tgt_lang = %s" % tgt_lang)

    lex = lexicon(src_lang, tgt_lang)

    ln_err = 0
    ln_sum = 0
    timer = time.time()

    fo = open(filename)
    fa = open(filename + ".flt.in", "w")
    fb = open(filename + ".flt.out", "w")
    fc = open(filename + ".flt.log", "w")

    for line in fo:
        error_log.clear()

        if line.count("\t") != 2:
            exit(line)
        idx, s0, t0 = line.split("\t")
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
        if not compare_findall(RE_PUNC, s1, t1):
            log_error("PUNCTUATION_MARK_MISMATCH")
        if not compare_findall(RE_BRACKET, s1, t1):
            log_error("BRACKET_MISMATCH")
        if not compare_findall(RE_QUOTATION, s1, t1):
            log_error("QUOTATION_MISMATCH")
        '''

        for txt, lang, side, in ((s1, src_lang, "SRC"), (t1, tgt_lang, "TGT")):

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

        s2 = tokenize(s1, src_lang)
        t2 = tokenize(t1, tgt_lang)

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

        m = lex.search(s2, t1)
        if None in m.values():
            print(s0)
            print(t0)
            print(m)
            input()

        '''
        src_nums = word_to_number(src, src_lang)
        tgt_nums = word_to_number(tgt, tgt_lang)
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

    fo.close()
    fa.close()
    fb.close()
    fc.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: %s src_lang tgt_lang corpus" % sys.argv[0])

    corpus_filter(*sys.argv[1:])
