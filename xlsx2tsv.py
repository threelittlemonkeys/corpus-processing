import sys
import xlrd

def xls2tsv(filename, option = None, sheet_idx = 0):
    workbook = xlrd.open_workbook(filename)

    if not option:
        print("\n".join(workbook.sheet_names()))
        return

    if option == "dump":
        for i in range(workbook.nsheets):
            fo = open("%s.tsv.sheet.%d" % (filename, i), "w")
            sheet = workbook.sheet_by_index(i)
            print_sheet(sheet, fo)
            fo.close()

    if option == "sheet":
        sheet = workbook.sheet_by_index(int(sheet_idx))
        print_sheet(sheet, sys.stdout)

def print_sheet(sheet, stream):
    # stream.write(sheet.name + "\n")
    for i in range(sheet.nrows):
        row = [str(sheet.cell_value(i, j)).strip() for j in range(sheet.ncols)]
        stream.write("%s\n" % "\t".join(row))

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3, 4]:
        sys.exit("Usage: %s filename dump|sheet sheet_idx" % sys.argv[0])
    xls2tsv(*sys.argv[1:])
