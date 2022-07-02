import sys
import re

def jamofy(s): # decompose Hangeul syllables into jamo
    o = ""
    I = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ" # initial consonants
    M = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ" # medial vowels
    F = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ" # final consonants
    for c in s:
        u = ord(c)
        if u < 0xAC00 or u > 0xD7A3: # if not Hangeul syllable
            o += c
            continue
        u -= 0xAC00
        f = u % 28 # final consonant
        m = u // 28 % 21 # medial vowel
        i = u // 28 // 21 # initial consonant
        o += I[i]
        o += M[m]
        if f > 0:
            o += F[f - 1]
    return o

if __name__ == "__main__":
    for line in sys.stdin:
        line = re.sub("\s", "", line)
        line = " ".join(line)
        print(jamofy(line))
    # text = "정 참판 양반댁 규수 큰 교자 타고 혼례 치른 날"
    # print(text)
    # print(jamofy(text))
