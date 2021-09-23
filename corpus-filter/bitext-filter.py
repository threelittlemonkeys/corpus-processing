from utils import *
from lexicon import bilingual_lexicon

if len(sys.argv) != 4:
    sys.exit("Usage: %s src_lang tgt_lang bitext" % sys.argv[0])

timer = time.time()
src_lang = sys.argv[1]
tgt_lang = sys.argv[2]
lang_pair = (src_lang, tgt_lang)
corpus = sys.argv[3]
lexicon = bilingual_lexicon(src_lang, tgt_lang)

global MAX_SENT_LEN
if set(lang_pair) & {"ja", "zh"}:
    MAX_SENT_LEN *= 2

fc = open(corpus)
fi = open(corpus + ".flt.in", "w")
fo = open(corpus + ".flt.out", "w")
fl = open(corpus + ".flt.log", "w")

for ln, line in enumerate(fc, 1):

    idx, s0, t0 = line.split("\t")

    s0 = s0.strip()
    t0 = t0.strip()
    s1 = normalize(s0)
    t1 = normalize(t0)
    s2 = tokenize(src_lang, s1)
    t2 = tokenize(tgt_lang, t1)
    err_log.clear()

    if s1 == "":
        log_error(ln, "SRC_EMPTY")
    if t1 == "":
        log_error(ln, "TGT_EMPTY")
    if s1 == t1:
        log_error(ln, "SRC_AND_TGT_IDENTICAL")
    elif src_lang != "en" and tgt_lang != "en":
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

    if len(s2) / len(t2) > SENT_LEN_RATIO:
        log_error(ln, "SRC_TOO_LONGER")
    if len(t2) / len(s2) > SENT_LEN_RATIO:
        log_error(ln, "TGT_TOO_LONGER")

    if len(s1) and len(t1):
        if s1[-1] not in EOS_PUNCS and t1[-1] in EOS_PUNCS:
            s0 += t1[-1]
            s1 += t1[-1]
        if s1[-1] in EOS_PUNCS and t1[-1] not in EOS_PUNCS:
            t0 += s1[-1]
            t1 += s1[-1]

    if diff_findall(RE_PUNC, s1, t1) > 1:
        log_error(ln, "PUNCTUATION_MARK_MISMATCH")
    if diff_findall(RE_BRACKET, s1, t1):
        log_error(ln, "BRACKET_MISMATCH")
    if diff_findall(RE_QUOTATION, s1, t1):
        log_error(ln, "QUOTATION_MISMATCH")

    for txt, lang, side, in ((s1, src_lang, "SRC"), (t1, tgt_lang, "TGT")):

        if RE_URL.search(txt):
            log_error(ln, "URL_IN_%s" % side)
        if RE_REPETITION.match(txt):
            log_error(ln, "%s_REPEATED" % side)
        if RE_INVALID_WORD.search(txt):
            log_error(ln, "INVALID_WORD_IN_%s" % side)

        if lang == "en" and not RE_LANG_EN.search(txt) \
        if lang == "ja" and not RE_LANG_JA.search(txt) \
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

    if lexicon.data:
        s3, t3 = lexicon.search(s2, t2)
        if len(s3) != len(t3):
            log_error(ln, "ENTITY_MISMATCH")
            '''
            print(ln, "src", s0, sep = "\t")
            print(ln, "tgt", t0, sep = "\t", end = "")
            for w in s3:
                if w not in t3:
                    print(ln, "", w, *s3[w], sep = "\t")
            print()
            '''

    if err_log:
        for err_code in err_log:
            print(err_code, line, sep = "\t", end = "", file = fo)
    else:
        print(idx, s0, t0, file = fi)

    if ln % 100000 == 0:
        print("%d sentence pairs" % ln, file = sys.stderr)

timer = time.time() - timer
ni = ln - len(err_cnt[0])
no = len(err_cnt[0])

print("SRC_LANG =", src_lang, file = fl)
print("TGT_LANG =", tgt_lang, file = fl)
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
