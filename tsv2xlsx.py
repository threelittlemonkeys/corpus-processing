import sys
import re
import xlsxwriter

def convert(x):
    try:
        return int(x)
    except:
        pass
    try:
        return float(x)
    except:
        pass
    return x

def tsv2xlsx(filename):
    fi = open(filename)
    fo = xlsxwriter.Workbook(filename + ".xlsx")
    worksheet = fo.add_worksheet()
    for i, row in enumerate(fi):
        for j, txt in enumerate(row.split("\t")):
            txt = re.sub("\s+", " ", txt)
            txt = txt.strip()
            txt = convert(txt)
            if len(txt) and txt[0] == "=":
                txt = "'" + txt
            worksheet.write(i, j, txt)
    fo.close()
    fi.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s filename" % sys.argv[0])
    tsv2xlsx(sys.argv[1])
