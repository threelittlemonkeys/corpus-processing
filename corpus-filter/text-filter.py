from utils import *

if len(sys.argv) != 3:
    sys.exit("Usage: %s lang bitext" % sys.argv[0])

timer = time.time()
lang = sys.argv[1]
corpus = sys.argv[2]

fc = open(corpus)
fi = open(corpus + ".flt.in", "w")
fo = open(corpus + ".flt.out", "w")
fl = open(corpus + ".flt.log", "w")

for ln, line in enumerate(fc, 1):

    s0 = line.strip()
    s1 = normalize(s0)
    s2 = tokenize(lang, s1)
    err_log.clear()

    if s1 == "":
        log_error(ln, "SRC_EMPTY")

    if len(s2) > MAX_SENT_LEN:
        log_error(ln, "SRC_TOO_LONG")
    if len(s2) < MIN_SENT_LEN:
        log_error(ln, "SRC_TOO_SHORT")

    if RE_URL.search(s1):
        log_error(ln, "URL_IN_SRC")
    if RE_INVALID_WORD.search(s1):
        log_error(ln, "INVALID_WORD_IN_SRC")

    if lang == "en" and not RE_LANG_EN.search(s1) \
    or lang == "ja" and not RE_LANG_JA.search(s1) \
    or lang == "ko" and not RE_LANG_KO.search(s1) \
    or lang == "ru" and not RE_LANG_RU.search(s1) \
    or lang == "zh" and not RE_LANG_ZH.search(s1):
        log_error(ln, "INVALID_SRC_LANGUAGE")

    if lang not in CJK_LANGS and RE_LANG_CJK.search(s1) \
    or lang == "en" and RE_LANG_RU.search(s1) \
    or lang == "ja" and RE_LANG_KO.search(s1) \
    or lang == "ko" and (RE_LANG_JA.search(s1) or RE_LANG_ZH.search(s1)) \
    or lang == "zh" and (RE_LANG_KO.search(s1) or RE_LANG_JA.search(s1)):
        log_error(ln, "INVALID_LANGUAGE_IN_SRC")

    if lang == "en" and RE_SENTS_EN.search(s1) \
    or lang == "ko" and RE_SENTS_KO.search(s1) \
    or lang == "zh" and RE_SENTS_ZH.search(s1):
        log_error(ln, "MULTIPLE_SENTENCES_IN_SRC")

    if any(map(lambda x: len(x) > MAX_WORD_LEN, s2)):
        log_error(ln, "LONG_WORD_IN_SRC")

    if err_log:
        for err_code in err_log:
            print(err_code, line, sep = "\t", end = "", file = fo)
    else:
        print(s0, file = fi)

    if ln % 100000 == 0:
        print("%d sentence pairs" % ln, file = sys.stderr)

timer = time.time() - timer
ni = ln - len(err_cnt[0])
no = len(err_cnt[0])

print("LANG =", lang, file = fl)
print("MAX_SENT_LEN =", MAX_SENT_LEN, file = fl)
print("MIN_SENT_LEN =", MIN_SENT_LEN, file = fl)
print("MAX_WORD_LEN =", MAX_WORD_LEN, file = fl)
print("SENT_LEN_RATIO =", SENT_LEN_RATIO, file = fl)
print(file = fl)

for code, cnt in sorted(err_cnt[1].items(), key = lambda x: -x[1]):
    print(code, cnt, "(%.4f%%)" % (cnt / ln * 100), file = fl)
print(file = fl)

print("%d sentence pairs in total" % ln, file = fl)
print("%d errors in total" % sum(err_cnt[1].values()), file = fl)
print("%d sentence pairs filtered in (%.4f%%)" % (ni, ni / ln * 100), file = fl)
print("%d sentence pairs filtered out (%.4f%%)" % (no, no / ln * 100), file = fl)
print("%f seconds" % timer, file = fl)

fc.close()
fi.close()
fo.close()
fl.close()
