import sys

def romanize(s):
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

if __name__ == "__main__":

    text = "정 참판 양반댁 규수 큰 교자 타고 혼례 치른 날"
    print(text)
    print(romanize(text))

    for line in sys.stdin:
        line = line.strip()
        print(line, romanize(line), sep = "\t")

