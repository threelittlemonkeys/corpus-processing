import sys
import time
from utils import *
from constants import *

if len(sys.argv) != 2:
    sys.exit("Usage: %s bitext" % sys.argv[0])

timer = time.time()

fo_raw = open(sys.argv[1])
fo_in = open(sys.argv[1] + ".in", "w")
fo_out = open(sys.argv[1] + ".out", "w")

for ln, line in enumerate(fo_raw, 1):
    idx, src, tgt = line.strip().split("\t")

    if ln % 100000 == 0:
        print("%d sentece pairs" % ln, file = sys.stderr)

    # quotation mark preprocessing 

    src = re.sub('"{2,}', '"', src)
    tgt = re.sub('"{2,}', '"', tgt)

    src_quot = find_quotes(src)
    tgt_quot = find_quotes(tgt)
    num_src_quot = len(src_quot)
    num_tgt_quot = len(tgt_quot)
    num_src_br = len(RE_FIND_BR.findall(src))
    num_tgt_br = len(RE_FIND_BR.findall(tgt))

    # bracket mismatch

    if num_src_br != num_tgt_br:
        print("BRACKET_MISMATCH", idx, src, tgt, sep = "\t", file = fo_out)
        continue

    # quotation mark match

    if num_src_quot == num_tgt_quot:
        print(idx, src, tgt, sep = "\t", file = fo_in)
        continue

    # quotation marks only at sentence ends

    src_quot_seo = find_quotes(src, seo = True)
    tgt_quot_seo = find_quotes(tgt, seo = True)

    if (not num_src_quot or src_quot_seo) and tgt_quot_seo \
    or ((not num_tgt_quot or tgt_quot_seo) and src_quot_seo):
        src = remove_indexed_str(src, src_quot_seo)
        tgt = remove_indexed_str(tgt, tgt_quot_seo)
        print(idx, src, tgt, sep = "\t", file = fo_in)
        continue

    if re.search("^[^%s]+[%s]+[^%s]+$" % (DQ, DQ, DQ), src) \
    or re.search("^[^%s]+[%s]+[^%s]+$" % (DQ, DQ, DQ), tgt):
        print(num_src_quot, src, tgt, sep = "\t")

    '''
    # only one quoted string in the sentence
    # find transliterated target phrase

    src_qstr = find_quoted_str(src, src_quot, qlen = 2)
    tgt_qstr = find_quoted_str(tgt, tgt_quot, qlen = 2)

    if (not num_src_quot or find_quot(src, seo = True)) and tgt_qstr:
        tr = find_transliteration(src, tgt_qstr[1])
        if tr[1] <= 3:
            print(src, tgt, sep = "\t")
            continue

    if (not num_tgt_quot or find_quot(tgt, seo = True)) and src_qstr:
        tr = find_transliteration(tgt, src_qstr[1])
        if tr[1] <= 3:
            print(src, tgt, sep = "\t")
            continue
    '''

    # TODO
    # sentence segmentation
    # quote extraction
    # MT source selection from HT text
    # calculate HT-MT simliarity

    print("UNKNOWN", src, tgt, sep = "\t", file = fo_out)
    continue

fo_raw.close()
fo_in.close()
fo_out.close()

timer = time.time() - timer

print("%f seconds" % timer, file = sys.stderr)
