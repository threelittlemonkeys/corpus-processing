from constants import *

def any_alnum(txt):
    return RE_ALNUM.search(txt)

def find_quotes(txt, seo = False):
    quotes = list()

    for w in RE_TOKENIZE_A.finditer(txt):
        i, j = w.start(), w.end()
        w = w.group().lower()
        for m in RE_FIND_QUOT.finditer(w):
            k = m.start()
            m = m.group()

            # double quote
            if m in DQ:
                quotes.append((i + k, m))
                continue

            # single quote
            if w in APOS_WORD:
                continue
            if w[k + 1:] in APOS_PRT:
                continue
            if k == 1 and w[0] in ("d" , "o"):
                continue
            if k == len(w) - 1 and (w[-2:-1] == "s" or w[-3:-1] == "in"):
                if not re.search("(^| )[%s]" % SQ, txt[:i]):
                    continue
                elif re.search("[%s]( |$)" % SQ, txt[j:]):
                    continue
            quotes.append((i + k, m))

    if seo: # at sentence ends only
        for x in quotes:
            if any_alnum(txt[:x[0]]) and any_alnum(txt[x[0] + 1:]):
                return

    return quotes

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

def find_transliteration(x, y):
    if RE_KO.search(x):
        x = romanize(x)
    if RE_KO.search(y):
        y = romanize(y)
    x = [w.group() for w in RE_TOKENIZE_B.finditer(x.lower())]
    y = y.lower()
    xs = []
    for z in (1, 2):
        for i in range(len(x) - z + 1):
            w = "".join(x[i:i + z])
            if RE_ALNUM.search(w):
                xs.append((w, edit_distance(w, y)))
    return min(xs, key = lambda x: x[1])

def romanize(s, norm = False):
    o = ""
    I = "g kk n d tt r m b pp s ss 0 j jj ch k t p h".split(" ") # initial consonants
    M = "a ae ya yae eo e yeo ye o wa wae oe yo u wo we wi yu eu ui i".split(" ") # medial vowels
    F = "k k k n n n t l k m l l l l l m p p t t ng t t k t p t".split(" ") # final consonants
    for c in s:
        u = ord(c)
        if u < 0xAC00 or u > 0xD7A3: # if not Hangeul syllable
            o += c
            continue
        u -= 0xAC00
        f = u % 28 # final consonant
        m = u // 28 % 21 # medial vowel
        i = u // 28 // 21 # initial consonant
        if i != 11:
            o += I[i]
        o += M[m]
        if f > 0:
            o += F[f - 1]
    return o

def edit_distance(a, b):
    Za = len(a) + 1
    Zb = len(b) + 1
    M = [[0 for i in range(Zb)] for j in range(Za)]
    for i in range(Za):
        M[i][0] = i
    for j in range(Zb):
        M[0][j] = j
    for i in range(1, Za):
        for j in range(1, Zb):
            M[i][j] = min(
                M[i - 1][j] + 1, # deletion
                M[i][j - 1] + 1, # insertion
                M[i - 1][j - 1] + (a[i - 1] != b[j - 1]) # substitution
            )
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]: # transposition
                M[i][j] = min(M[i][j], M[i - 2][j - 2] + 1)
    return M[-1][-1]
