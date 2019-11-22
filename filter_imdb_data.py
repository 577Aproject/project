# useage: filter duplicate imdb movies. 
# The first argument is the file to filter. The second file is the output file.

import csv
import sys

if __name__ == "__main__":

    csv.field_size_limit(sys.maxsize)
    filter_file = open(sys.argv[2], 'w')
    tsv_writer = csv.writer(filter_file, delimiter='\t')

    with open(sys.argv[1]) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        tsv_writer.writerow(next(reader))
        for row in reader:
            if row[3] != 'US':
                continue
            tsv_writer.writerow(row)

    filter_file.close()
