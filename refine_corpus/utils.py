from constants import *

def find_quotes(txt, seo = False):
    quotes = list()

    for w in RE_TOKEN.finditer(txt):
        w, i, j = w.group().lower(), w.start(), w.end()

        for m in RE_QUOT.finditer(w):
            m, k = m.group(), m.start()

            # double quote

            if m in DQ:
                quotes.append((i + k, m))
                continue

            # single quote

            if 0 < k < len(w) - 1 and w in CTR_WORD:
                continue

            if k == 0 and w in CTR_L:
                continue

            if 0 < k < len(w) - 1 and CTR_R.search(w):
                continue

            if k == len(w) - 1 and re.search(".{2}(in|s).$", w):
                if not re.search("(^| )[%s]" % SQ, txt[:i]):
                    continue
                if re.search("[%s]( |$)" % SQ, txt[j:]):
                    continue

            quotes.append((i + k, m))

    if seo: # at sentence ends only
        for x in quotes:
            if RE_ALNUM.search(txt[:x[0]]) and RE_ALNUM.search(txt[x[0] + 1:]):
                return

    return quotes

def remove_matched_strs(txt, ms):
    k = 0
    for i, m in ms:
        i += k
        txt = txt[:i] + txt[i + len(m):]
        k -= len(m)
    txt = re.sub("  +", " ", txt.strip())
    return txt

def find_quoted_str(txt, quotes, qlen):
    if len(quotes) != 2:
        return
    i, j = quotes[0][0], quotes[1][0]
    if i > 0 and RE_ALNUM.search(txt[i - 1]):
        return
    qstr = txt[i + 1:j].strip()
    if not qstr:
        return
    if qstr.count(" ") > qlen - 1:
        return
    return (i, qstr)

def replace_quoted_str(x, y, x_qstr):
    i, x_qstr = x_qstr
    pt = re.compile(r"[%s]*%s[%s]*" % (QUOT, re.escape(x_qstr), QUOT), re.I)
    if len(pt.findall(y)) == 1:
        x_qstr = x[i:i + len(x_qstr) + 2]
        y_qstr = pt.search(y).group()
        y = y.replace(y_qstr, x_qstr)
    return x, y
