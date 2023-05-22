import sys
import re
import openpyxl

def xls2tsv(filename, option = None, sheet_idx = 0):

    workbook = openpyxl.load_workbook(filename)
    sheet_idx = int(sheet_idx)

    if not option:
        print("\n".join(workbook.sheetnames))
        return

    if option == "dump":
        for sheet_idx, sheet in enumerate(workbook._sheets):
            fo = open("%s.sheet_%d.%s.tsv" % (filename, sheet_idx, sheet.title), "w")
            print_sheet(sheet, fo)
            fo.close()

    if option == "sheet":
        sheet = workbook._sheets[sheet_idx]
        fo = open("%s.sheet_%d.%s.tsv" % (filename, sheet_idx, sheet.title), "w")
        print_sheet(sheet, fo)
        fo.close()

def print_sheet(sheet, fo):
    for row in sheet.values:
        row = [str(col if col != None else "").strip().replace("\n", "\\n") for col in row]
        fo.write("%s\n" % "\t".join(row))

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3, 4]:
        sys.exit("Usage: %s filename dump|sheet sheet_idx" % sys.argv[0])
    xls2tsv(*sys.argv[1:])
