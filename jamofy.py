import sys
import re

def jamofy(s): # decompose Hangeul syllables into jamo
    o = ""
    ic = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ" # initial consonants
    mv = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ" # medial vowels
    fc = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ" # final consonants
    for c in s:
        u = ord(c)
        if u < 0xAC00 or u > 0xD7A3: # if not Hangeul syllable
            o += c
            continue
        u -= 0xAC00
        f = u % 28 # final consonant
        m = u // 28 % 21 # medial vowel
        i = u // 28 // 21 # initial consonant
        o += ic[i]
        o += mv[m]
        if f:
            o += fc[f]
    return o

if __name__ == "__main__":

    '''
    text = "정 참판 양반댁 규수 큰 교자 타고 혼례 치른 날"
    print(text)
    print(jamofy(text))
    '''

    for line in sys.stdin:
        line = re.sub("\s", "", line)
        line = " ".join(line)
        print(jamofy(line))
