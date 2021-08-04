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
