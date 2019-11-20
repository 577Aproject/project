import csv
import sys

csv.field_size_limit(sys.maxsize)

filter_file = open('/Users/jasper/Downloads/filter.tsv', 'w')
tsv_writer = csv.writer(filter_file, delimiter='\t')

with open('/Users/jasper/Downloads/movie_titles.tsv') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    tsv_writer.writerow(next(reader))
    for row in reader:
        if row[3] != 'US':
            continue
        tsv_writer.writerow(row)

filter_file.close()