import sys
import re
import xlsxwriter

def tsv2xlsx(filename):
    fi = open(filename)
    fo = xlsxwriter.Workbook(filename + ".xlsx")
    worksheet = fo.add_worksheet()
    for idx, text in enumerate(fi):
        _text = []
        for x in text.split("\t"):
            x = re.sub("[\x00-\x20]+", " ", x)
            x = x.strip()
            x = re.sub('^(=|"|https?://)', "'\\1", x)
            _text.append(x)
        worksheet.write_row(idx, 0, _text)
    fo.close()
    fi.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s filename" % sys.argv[0])
    tsv2xlsx(sys.argv[1])
