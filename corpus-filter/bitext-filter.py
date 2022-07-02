from utils import *

if len(sys.argv) not in (2, 3):
    sys.exit("Usage: %s clean_bitext (raw_bitext)" % sys.argv[0])

fa = open(sys.argv[1])
fb = open(sys.argv[2]) if len(sys.argv) == 3 else None

timer = time.time()
filename = sys.argv[-1]

fi = open(filename + ".flt.in", "w")
fo = open(filename + ".flt.out", "w")
fl = open(filename + ".flt.log", "w")

for ln, line in enumerate(fa, 1):

    *idx, s0, t0 = line.split("\t")

    s0 = s0.strip()
    t0 = t0.strip()
    s1 = normalize(s0)
    t1 = normalize(t0)
    s2 = tokenize(SRC_LANG, s1)
    t2 = tokenize(TGT_LANG, t1)
    err_log.clear()

    if s1 == "":
        log_error(ln, "SRC_EMPTY")
    if t1 == "":
        log_error(ln, "TGT_EMPTY")
    if s1 == t1:
        log_error(ln, "SRC_AND_TGT_IDENTICAL")
    elif SRC_LANG != "en" and TGT_LANG != "en":
        if s1 in t1:
            log_error(ln, "SRC_IN_TGT")
        if t1 in s1:
            log_error(ln, "TGT_IN_SRC")

    if len(s2) > MAX_SENT_LEN:
        log_error(ln, "SRC_TOO_LONG")
    if len(t2) > MAX_SENT_LEN:
        log_error(ln, "TGT_TOO_LONG")
    if len(s2) < MIN_SENT_LEN:
        log_error(ln, "SRC_TOO_SHORT")
    if len(t2) < MIN_SENT_LEN:
        log_error(ln, "TGT_TOO_SHORT")

    if len(t2) == 0 or (len(s2) + 5) / (len(t2) + 5) > SENT_LEN_RATIO:
        log_error(ln, "SRC_TOO_LONGER")
    if len(s2) == 0 or (len(t2) + 5) / (len(s2) + 5) > SENT_LEN_RATIO:
        log_error(ln, "TGT_TOO_LONGER")

    if LS_MISMATCH and len(findall_diff(RE_LS, s1, t1)) >= LS_MISMATCH:
        log_error(ln, "LIST_MARKER_MISMATCH")
    if SYM_MISMATCH and len(findall_diff(RE_SYM, s1, t1)) >= SYM_MISMATCH:
        log_error(ln, "SYMBOL_MISMATCH")
    if BR_MISMATCH and len(findall_diff(RE_BR, s1, t1)) >= BR_MISMATCH:
        log_error(ln, "BRACKET_MISMATCH")
    if PUNC_MISMATCH and len(findall_diff(RE_PUNC, s1, t1)) >= PUNC_MISMATCH:
        log_error(ln, "PUNCTUATION_MARK_MISMATCH")
    if QUOT_MISMATCH and len(findall_diff(count_quotes, s1, t1)) >= QUOT_MISMATCH:
        log_error(ln, "QUOTATION_MISMATCH")
    if NUM_MISMATCH and len(findall_diff(count_nums, s1, t1)) >= NUM_MISMATCH:
        log_error(ln, "NUMBER_MISMATCH")

    pairs = ((s1, SRC_LANG, "SRC"), (t1, TGT_LANG, "TGT"))
    for txt, lang, side, in pairs:

        if RE_URL.search(txt):
            log_error(ln, "URL_IN_%s" % side)
        if RE_REPETITION.match(txt):
            log_error(ln, "%s_REPEATED" % side)

        if lang == "en" and not RE_LANG_EN.search(txt) \
        or lang == "ja" and not RE_LANG_JA.search(txt) \
        or lang == "ko" and not RE_LANG_KO.search(txt) \
        or lang == "ru" and not RE_LANG_RU.search(txt) \
        or lang == "zh" and not RE_LANG_ZH.search(txt):
            log_error(ln, "INVALID_%s_LANGUAGE" % side)

        if lang not in CJK_LANGS and RE_LANG_CJK.search(txt) \
        or lang == "ja" and RE_LANG_KO.search(txt) \
        or lang == "ko" and (RE_LANG_JA.search(txt) or RE_LANG_ZH.search(txt)) \
        or lang == "zh" and (RE_LANG_KO.search(txt) or RE_LANG_JA.search(txt)):
            log_error(ln, "INVALID_LANGUAGE_IN_%s" % side)

        if lang == "en" and RE_SENTS_EN.search(txt) \
        or lang == "ko" and RE_SENTS_KO.search(txt) \
        or lang == "zh" and RE_SENTS_ZH.search(txt):
            log_error(ln, "MULTIPLE_SENTENCES_IN_%s" % side)

    if any(map(lambda x: len(x) > MAX_WORD_LEN, s2)):
        log_error(ln, "LONG_WORD_IN_SRC")
    if any(map(lambda x: len(x) > MAX_WORD_LEN, t2)):
        log_error(ln, "LONG_WORD_IN_TGT")

    if ln % 100000 == 0:
        print("%d sentence pairs" % ln, file = sys.stderr)

    if fb:
        line = next(fb)

    if not err_log:
        print(line, sep = "\t", end = "", file = fi)

    for err_code in err_log:
        print(err_code, line, sep = "\t", end = "", file = fo)

timer = time.time() - timer
ni = ln - len(err_cnt[0])
no = len(err_cnt[0])

print("SRC_LANG =", SRC_LANG, file = fl)
print("TGT_LANG =", TGT_LANG, file = fl)
print("MAX_SENT_LEN =", MAX_SENT_LEN, file = fl)
print("MIN_SENT_LEN =", MIN_SENT_LEN, file = fl)
print("MAX_WORD_LEN =", MAX_WORD_LEN, file = fl)
print("SENT_LEN_RATIO =", SENT_LEN_RATIO, file = fl)
print("LS_MISMATCH =", LS_MISMATCH, file = fl)
print("SYM_MISMATCH =", SYM_MISMATCH, file = fl)
print("BR_MISMATCH =", BR_MISMATCH, file = fl)
print("PUNC_MISMATCH =", PUNC_MISMATCH, file = fl)
print("QUOT_MISMATCH =", QUOT_MISMATCH, file = fl)

print(file = fl)

for code, cnt in sorted(err_cnt[1].items(), key = lambda x: -x[1]):
    print(code, cnt, "(%.4f%%)" % (cnt / ln * 100), file = fl)
print(file = fl)

print("%d sentence pairs in total" % ln, file = fl)
print("%d errors in total" % sum(err_cnt[1].values()), file = fl)
print("%d sentence pairs filtered in (%.4f%%)" % (ni, ni / ln * 100), file = fl)
print("%d sentence pairs filtered out (%.4f%%)" % (no, no / ln * 100), file = fl)
print("%f seconds" % timer, file = fl)

fa.close()
if fb != None:
    fb.close()

fi.close()
fo.close()
fl.close()
