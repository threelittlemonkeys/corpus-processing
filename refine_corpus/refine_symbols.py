import sys
import time
from utils import *

fo = open(sys.argv[1])

for ln, line in enumerate(fo, 1):

    *idx, src, tgt = line.strip().split("\t")

    if ln % 100000 == 0:
        print("%d sentece pairs" % ln, file = sys.stderr)

    # preprocessing

    src = re.sub(" (?=,)", "", src)
    tgt = re.sub(" (?=,)", "", tgt)
    src = re.sub("(?<=,)(?=[^ 0-9,'\"])", " ", src)
    tgt = re.sub("(?<=,)(?=[^ 0-9,'\" ])", " ", tgt)
    src = re.sub(" (?=[%s],)" % re.escape(QUOT), "", src)
    tgt = re.sub(" (?=[%s],)" % re.escape(QUOT), "", tgt)

    # quotation marks only at sentence ends

    src_quot = find_quotes(src)
    tgt_quot = find_quotes(tgt)
    num_src_quot = len(src_quot)
    num_tgt_quot = len(tgt_quot)
    src_quot_seo = find_quotes(src, seo = True)
    tgt_quot_seo = find_quotes(tgt, seo = True)

    if (not num_src_quot or src_quot_seo) and tgt_quot_seo \
    or ((not num_tgt_quot or tgt_quot_seo) and src_quot_seo):
        src = remove_matched_strs(src, src_quot_seo)
        tgt = remove_matched_strs(tgt, tgt_quot_seo)

    # punctuation marks at end of sentence

    src_pq_eos = RE_PQ_EOS.search(src)
    tgt_pq_eos = RE_PQ_EOS.search(tgt)
    
    if bool(src_pq_eos) ^ bool(tgt_pq_eos):
        if src_pq_eos and not RE_QUOT.search(src_pq_eos.group()):
            tgt += src_pq_eos.group()
        if tgt_pq_eos and not RE_QUOT.search(tgt_pq_eos.group()):
            src += tgt_pq_eos.group()

    # quoted strings

    src_quot = find_quotes(src)
    tgt_quot = find_quotes(tgt)
    src_qstr = find_quoted_str(src, src_quot, qlen = 3)
    tgt_qstr = find_quoted_str(tgt, tgt_quot, qlen = 3)

    if bool(src_qstr) ^ bool(tgt_qstr):
        if src_qstr:
            _src, _tgt = replace_quoted_str(src, tgt, src_qstr)
        if tgt_qstr:
            _tgt, _src = replace_quoted_str(tgt, src, tgt_qstr)
        src = _src
        tgt = _tgt

    print(*idx, src, tgt, sep = "\t")
    continue

fo.close()
