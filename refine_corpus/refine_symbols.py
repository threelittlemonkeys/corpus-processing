import sys
import time
from utils import *
from constants import *

fo = open(sys.argv[1])
timer = time.time()

for ln, line in enumerate(fo, 1):

    *idx, src, tgt = line.strip().split("\t")

    if ln % 100000 == 0:
        print("%d sentece pairs" % ln, file = sys.stderr)

    # preprocessing

    src = re.sub("([%s])\\1+" % re.escape(QUOT), '\\1', src)
    tgt = re.sub("([%s])\\1+" % re.escape(QUOT), '\\1', tgt)
    src = re.sub(" (?=,)", "", src)
    tgt = re.sub(" (?=,)", "", tgt)
    src = re.sub("(?<=,)(?=[^, ])", " ", src)
    tgt = re.sub("(?<=,)(?=[^, ])", " ", tgt)
    src = re.sub(" (?=[%s],)" % re.escape(QUOT), "", src)
    tgt = re.sub(" (?=[%s],)" % re.escape(QUOT), "", tgt)

    # symbol mismatch

    num_src_sym = len(RE_FIND_SYM.findall(src))
    num_tgt_sym = len(RE_FIND_SYM.findall(tgt))

    if num_src_sym != num_tgt_sym:
        print(*idx, src, tgt, "SYMBOL_MISMATCH", sep = "\t")
        continue

    # bracket mismatch

    num_src_br = len(RE_FIND_BR.findall(src))
    num_tgt_br = len(RE_FIND_BR.findall(tgt))

    if num_src_br != num_tgt_br:
        print(*idx, src, tgt, "BRACKET_MISMATCH", sep = "\t")
        continue

    # punctuation mark mismatch

    src_punc_eos = RE_FIND_PUNC_EOS.search(src)
    tgt_punc_eos = RE_FIND_PUNC_EOS.search(tgt)
    
    if src_punc_eos and not tgt_punc_eos or not src_punc_eos and tgt_punc_eos:
        if src_punc_eos:
            tgt += src_punc_eos.group()
        if tgt_punc_eos:
            src += tgt_punc_eos.group()

    # quotation mark match

    src_quot = find_quotes(src)
    tgt_quot = find_quotes(tgt)
    num_src_quot = len(src_quot)
    num_tgt_quot = len(tgt_quot)

    if num_src_quot == num_tgt_quot:
        print(*idx, src, tgt, sep = "\t")
        continue

    # quotation marks only at sentence ends

    src_quot_seo = find_quotes(src, seo = True)
    tgt_quot_seo = find_quotes(tgt, seo = True)

    if (not num_src_quot or src_quot_seo) and tgt_quot_seo \
    or ((not num_tgt_quot or tgt_quot_seo) and src_quot_seo):
        src = remove_matched_strs(src, src_quot_seo)
        tgt = remove_matched_strs(tgt, tgt_quot_seo)
        print(*idx, src, tgt, sep = "\t")
        continue

    # quoted strings

    src_qstr = find_quoted_str(src, src_quot, qlen = 3)
    tgt_qstr = find_quoted_str(tgt, tgt_quot, qlen = 3)

    if len(src_qstr) ^ len(tgt_qstr):
        if src_qstr:
            _src, _tgt = sub_quoted_str(src, tgt, src_qstr)
        if tgt_qstr:
            _tgt, _src = sub_quoted_str(tgt, src, tgt_qstr)
        if src != _src or tgt != _tgt:
            src, tgt = _src, _tgt
            print(*idx, src, tgt, sep = "\t")
            continue

    print(*idx, src, tgt, "MISCELLANEOUS", sep = "\t")

fo.close()
timer = time.time() - timer
print("%f seconds" % timer, file = sys.stderr)
