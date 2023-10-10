import unicodedata

def ulen(x): # unicode string length

    if type(x) != str:
        return 0

    return sum(1 + (unicodedata.east_asian_width(c) in "FW") for c in x)
