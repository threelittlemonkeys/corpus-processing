import re
import unicodedata

def normalize_html(html):
    
    html = re.sub("&nbsp;", " ", html)
    html = re.sub("\s+", " ", html)
    html = html.strip()

    return html


def ulen(x): # unicode string length

    if type(x) != str:
        return 0

    return sum(1 + (unicodedata.east_asian_width(c) in "FW") for c in x)
