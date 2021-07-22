from utils import *
from lexicon import bilingual_lexicon

def corpus_filter(src_lang, tgt_lang, filename):

    print("src_lang = %s" % src_lang, file = sys.stderr)
    print("tgt_lang = %s" % tgt_lang, file = sys.stderr)

    fo = open(filename)
    fa = open(filename + ".flt.in", "w")
    fb = open(filename + ".flt.out", "w")
    fc = open(filename + ".flt.log", "w")

    timer = time.time()
    lexicon = bilingual_lexicon(src_lang, tgt_lang)
    num_errs = 0

    for ln, line in enumerate(fo, 1):

        if line.count("\t") != 2:
            s0, t0 = line.split("\t")
        else:
            idx, s0, t0 = line.split("\t")

        s1 = normalize(s0)
        t1 = normalize(t0)
        err_log.clear()

        if s1 == "":
            log_error("SRC_EMPTY")
        if t1 == "":
            log_error("TGT_EMPTY")
        if s1 == t1:
            log_error("SRC_AND_TGT_IDENTICAL")
        elif src_lang not in EU_LANGS and tgt_lang not in EU_LANGS:
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

            if lang in EU_LANGS and RE_LANG_CJK.search(txt) \
            or lang == "ja" and RE_LANG_KO.search(txt) \
            or lang == "ko" and (RE_LANG_JA.search(txt) or RE_LANG_ZH.search(txt)) \
            or lang == "zh" and (RE_LANG_KO.search(txt) or RE_LANG_JA.search(txt)):
                log_error("INVALID_LANGUAGE_IN_%s" % side)

            if lang == "en" and RE_SENTS_EN.search(txt) \
            or lang == "ko" and RE_SENTS_KO.search(txt) \
            or lang == "zh" and RE_SENTS_ZH.search(txt):
                log_error("MULTIPLE_SENTENCES_IN_%s" % side)

        s2 = tokenize(s1)
        t2 = tokenize(t1)

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

        if lexicon.data:
            s3, t3 = "", ""
            if src_lang == "en" and tgt_lang == "es":
                s3, t3 = s2, t2
            if src_lang == "en" and tgt_lang == "ko":
                s3, t3 = s2, re.sub("(?<=[^a-z]) (?=[a-z])", "", t1)
            s3, t3 = lexicon.search(s3, t3)

            if len(s3) != len(t3):
                log_error("ENTITY_MISMATCH")
                print(ln, "src", s1, sep = "\t")
                print(ln, "tgt", t1, sep = "\t")
                for w in s3:
                    if w not in t3:
                        print(ln, "", w, *s3[w], sep = "\t")
                print()

        if err_log:
            for err_code in err_log:
                print(err_code, line, sep = "\t", end = "", file = fb)
            num_errs += 1
        else:
            print(line, end = "", file = fa)

        if ln % 100000 == 0:
            print("%d sentence pairs" % ln, file = sys.stderr)

    timer = time.time() - timer

    for code, cnt in sorted(err_cnt.items(), key = lambda x: -x[1]):
        print(code, cnt, "(%.4f%%)" % (cnt / ln * 100), file = fc)
    print(file = fc)
    print("%d sentence pairs in total" % ln, file = fc)
    print("%d sentence pairs filtered out (%.4f%%)" % (num_errs, num_errs / ln * 100), file = fc)
    print("%f seconds" % timer, file = fc)

    fo.close()
    fa.close()
    fb.close()
    fc.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: %s src_lang tgt_lang bitext" % sys.argv[0])

    corpus_filter(*sys.argv[1:])
