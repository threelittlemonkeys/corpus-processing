import sys
import csv
import xlsxwriter

def xlsx2tsv(filename):
    workbook = xlsxwriter.Workbook(filename + ".xlsx")
    worksheet = workbook.add_worksheet()
    tsv = csv.reader(open(filename), delimiter = "\t")
    for row_idx, row_text in enumerate(tsv):
        row_text = row_text.replace('"', '""')
        worksheet.write_row(row_idx, 0, row_text)
    workbook.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s filename" % sys.argv[0])
    xlsx2tsv(sys.argv[1])
