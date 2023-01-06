from utils import *
sys.path.append("../xl_tokenizer")
from tokenizer import normalize, tokenize

if len(sys.argv) not in (2, 3):
    sys.exit("Usage: %s clean_bitext (raw_bitext)" % sys.argv[0])

print_parameters(sys.stderr)

timer = time.time()
logger = logger()
filename = sys.argv[1]

if DICT_MISMATCH:
    ent_dict = load_dict(DICT_PATH)

fo_in = open(filename + ".flt.in", "w")
fo_out = open(filename + ".flt.out", "w")
fo_log = open(filename + ".flt.log", "w")
fo_clean = open(filename)
fo_raw = open(sys.argv[2]) if len(sys.argv) == 3 else None

for ln, line in enumerate(fo_clean, 1):

    *idx, x0, y0 = line.split("\t")

    x0 = x0.strip()
    y0 = y0.strip()
    x1 = normalize(x0)
    y1 = normalize(y0)
    x2 = tokenize(SRC_LANG, x1)
    y2 = tokenize(TGT_LANG, y1)
    logger.errors.clear()

    if x1 == "":
        logger.log(ln, "SRC_EMPTY")
    if y1 == "":
        logger.log(ln, "TGT_EMPTY")
    if x1 == y1:
        logger.log(ln, "SRC_AND_TGT_IDENTICAL")
    elif SRC_LANG != "en" and TGT_LANG != "en":
        if x1 in y1:
            logger.log(ln, "SRC_IN_TGT")
        if y1 in x1:
            logger.log(ln, "TGT_IN_SRC")

    if len(x2) > MAX_SENT_LEN:
        logger.log(ln, "SRC_TOO_LONG")
    if len(y2) > MAX_SENT_LEN:
        logger.log(ln, "TGT_TOO_LONG")
    if len(x2) < MIN_SENT_LEN:
        logger.log(ln, "SRC_TOO_SHORT")
    if len(y2) < MIN_SENT_LEN:
        logger.log(ln, "TGT_TOO_SHORT")

    if len(y2) == 0 or (len(x2) + 5) / (len(y2) + 5) > SENT_LEN_RATIO:
        logger.log(ln, "SRC_TOO_LONGER")
    if len(x2) == 0 or (len(y2) + 5) / (len(x2) + 5) > SENT_LEN_RATIO:
        logger.log(ln, "TGT_TOO_LONGER")

    if LS_MISMATCH and len(findall_diff(RE_LS, x1, y1)) >= LS_MISMATCH:
        logger.log(ln, "LIST_MARKER_MISMATCH")
    if SYM_MISMATCH and len(findall_diff(RE_SYM, x1, y1)) >= SYM_MISMATCH:
        logger.log(ln, "SYMBOL_MISMATCH")
    if BR_MISMATCH and len(findall_diff(RE_BR, x1, y1)) >= BR_MISMATCH:
        logger.log(ln, "BRACKET_MISMATCH")
    if PUNC_MISMATCH and len(findall_diff(RE_PUNC, x1, y1)) >= PUNC_MISMATCH:
        logger.log(ln, "PUNCTUATION_MARK_MISMATCH")
    if QUOT_MISMATCH and len(findall_diff(count_quotes, x1, y1)) >= QUOT_MISMATCH:
        logger.log(ln, "QUOTATION_MARK_MISMATCH")

    if ALPHA_MISMATCH and len(findall_diff(RE_ALPHA, x1, y1)) >= ALPHA_MISMATCH:
        logger.log(ln, "ALPHABET_MISMATCH")
    if NUM_MISMATCH and len(findall_diff(count_nums, x1, y1)) >= NUM_MISMATCH:
        logger.log(ln, "NUMBER_MISMATCH")
    if DICT_MISMATCH and len(match_dict(ent_dict, x1, y1)[1]) >= DICT_MISMATCH:
        logger.log(ln, "DICTIONARY_MISMATCH")

    pairs = ((x1, SRC_LANG, "SRC"), (y1, TGT_LANG, "TGT"))

    for txt, lang, side, in pairs:

        if RE_URL.search(txt):
            logger.log(ln, "URL_IN_%s" % side)
        if RE_INVALID_CHAR.search(txt):
            logger.log(ln, "INVALID_CHARACTER_IN_%s" % side)
        if RE_REPETITION.search(txt):
            logger.log(ln, "REPETITION_IN_%s" % side)

        if lang == "en" and not RE_LANG_EN.search(txt) \
        or lang == "ja" and not RE_LANG_JA.search(txt) \
        or lang == "ko" and not RE_LANG_KO.search(txt) \
        or lang == "ru" and not RE_LANG_RU.search(txt) \
        or lang == "zh" and not RE_LANG_ZH.search(txt):
            logger.log(ln, "INVALID_%s_LANGUAGE" % side)

        if lang not in CJK_LANGS and RE_LANG_CJK.search(txt) \
        or lang == "ja" and RE_LANG_KO.search(txt) \
        or lang == "ko" and (RE_LANG_JA.search(txt) or RE_LANG_ZH.search(txt)) \
        or lang == "zh" and (RE_LANG_KO.search(txt) or RE_LANG_JA_KANA.search(txt)):
            logger.log(ln, "INVALID_LANGUAGE_IN_%s" % side)

        if lang == "en" and RE_SENTS_EN.search(txt) \
        or lang == "ko" and RE_SENTS_KO.search(txt) \
        or lang == "zh" and RE_SENTS_ZH.search(txt):
            logger.log(ln, "MULTIPLE_SENTENCES_IN_%s" % side)

    if any(map(lambda x: len(x) > MAX_WORD_LEN, x2)):
        logger.log(ln, "LONG_WORD_IN_SRC")
    if any(map(lambda x: len(x) > MAX_WORD_LEN, y2)):
        logger.log(ln, "LONG_WORD_IN_TGT")

    if ln % 100000 == 0:
        print("%d sentence pairs" % ln, file = sys.stderr)

    if fo_raw:
        line = next(fo_raw)

    if not logger.errors:
        print(line, sep = "\t", end = "", file = fo_in)

    for error_code in logger.errors:
        print(error_code, line, sep = "\t", end = "", file = fo_out)

num_ins = ln - len(logger.lines)
num_outs = len(logger.lines)
timer = time.time() - timer

print_parameters(fo_log)
print(file = fo_log)

for error_code, count in sorted(logger.cats.items(), key = lambda x: -x[1]):
    print(error_code, count, "(%.4f%%)" % (count / ln * 100), file = fo_log)
print(file = fo_log)

print("%d sentence pairs in total" % ln, file = fo_log)
print("%d errors in total" % sum(logger.cats.values()), file = fo_log)
print("%d sentence pairs filtered in (%.4f%%)" % (num_ins, num_ins / ln * 100), file = fo_log)
print("%d sentence pairs filtered out (%.4f%%)" % (num_outs, num_outs / ln * 100), file = fo_log)
print("%f seconds" % timer, file = fo_log)

fo_in.close()
fo_out.close()
fo_log.close()
fo_clean.close()
fo_raw.close() if fo_raw else None
