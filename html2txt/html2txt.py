import sys
import re
from table import *

def html2txt(filename):

    with open(filename) as fo:

        html = fo.read()
        html = re.sub("\s+", " ", html).strip()

        for pos, table in find_tables(html):
            txt = print_table(table)
            print(txt)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Usage: %s filename" % sys.argv[0])

    html2txt(sys.argv[1])
