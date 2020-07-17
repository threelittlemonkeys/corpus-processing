import sys
import xlrd

def xls2tsv(filename, option = None, sheet_idx = 0):
    workbook = xlrd.open_workbook(filename)
    sheet_idx = int(sheet_idx)

    if not option:
        print("\n".join(workbook.sheet_names()))
        return

    if option == "dump":
        for sheet_idx in range(workbook.nsheets):
            sheet = workbook.sheet_by_index(sheet_idx)
            fo = open("%s.sheet_%d.%s.tsv" % (filename, sheet_idx, sheet.name), "w")
            print_sheet(sheet, fo)
            fo.close()

    if option == "sheet":
        sheet = workbook.sheet_by_index(sheet_idx)
        fo = open("%s.sheet_%d.%s.tsv" % (filename, sheet_idx, sheet.name), "w")
        print_sheet(sheet, fo)
        fo.close()

def print_sheet(sheet, stream):
    for i in range(sheet.nrows):
        row = [str(sheet.cell_value(i, j)).strip() for j in range(sheet.ncols)]
        stream.write("%s\n" % "\t".join(row))

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3, 4]:
        sys.exit("Usage: %s filename dump|sheet sheet_idx" % sys.argv[0])
    xls2tsv(*sys.argv[1:])
