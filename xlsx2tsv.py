import sys
import re
import math
import pandas as pd

def xls2tsv(filename, option = None, sheet_idx = 0):

    sheets = pd.read_excel(io = filename, sheet_name = None, header = None)

    if not option:

        print("\n".join(sheets.keys()))
        return

    if option == "dump":

        for sheet_idx, (sheet_name, sheet) in enumerate(sheets.items()):
            fo = open("%s.sheet_%d.%s.tsv" % (filename, sheet_idx, sheet_name), "w")
            print_sheet(fo, sheet)
            fo.close()
        return

    if option == "sheet":

        sheet_idx = int(sheet_idx)
        sheet_name = [*sheets.keys()][sheet_idx]
        sheet = sheets[sheet_name]
        fo = open("%s.sheet_%d.%s.tsv" % (filename, sheet_idx, sheet_name), "w")
        print_sheet(fo, sheet)
        fo.close()
        return

def print_sheet(fo, sheet):

    sheet = sheet.replace({float("NaN"): None})

    for row_idx, row in sheet.iterrows():

        row = [
            re.sub(r"\s+", " ",
                str("" if col == None else col)
                .replace("\t", "\\t")
                .replace("\n", "\\n")
            ).strip()
            for col in row
        ]

        print("\t".join(row), file = fo)

if __name__ == "__main__":

    if len(sys.argv) not in [2, 3, 4]:
        sys.exit("Usage: %s filename dump|sheet sheet_idx" % sys.argv[0])

    xls2tsv(*sys.argv[1:])
