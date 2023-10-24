import sys
from html_parser import *

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Usage: %s filename" % sys.argv[0])

    with open(sys.argv[1]) as fo:

        html = fo.read()
        text = html_to_text(html)
