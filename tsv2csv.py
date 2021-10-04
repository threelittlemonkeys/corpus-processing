import sys
import csv

if len(sys.argv) != 2:
    sys.exit("Usage: %s tsv_file")

with open(sys.argv[1]) as fin:
    with open(sys.argv[1] + ".csv", "w") as fout:
        data = csv.reader(fin, delimiter = "\t")
        writer = csv.writer(fout, lineterminator = "\n")
        for line in data:
            writer.writerow(line)
