import sys
import re
import xlsxwriter

def tsv2xlsx(filename):
    fi = open(filename)
    fo = xlsxwriter.Workbook(filename + ".xlsx")
    worksheet = fo.add_worksheet()
    for i, row in enumerate(fi):
        for j, col in enumerate(row.split("\t")):
            col = col.strip()
            worksheet.write(i, j, col)
    fo.close()
    fi.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s filename" % sys.argv[0])
    tsv2xlsx(sys.argv[1])
