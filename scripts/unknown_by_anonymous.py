#!usr/bin/env python3

import csv
from collections import namedtuple

Data = namedtuple(
    'Data',
    ['headers', 'rows']
)


def get_unknown_by_anonymous(in_file):
    with open(in_file) as f:
        reader = csv.DictReader(f)
        # separate headers and data to persist both for writing
        headers = reader.fieldnames
        return Data(headers, list(reader))


def write_unknown_by_anonymous(out_file, data):
        writer = csv.DictWriter(open(out_file, 'w'), fieldnames=data.headers)
        writer.writeheader()
        for row in data.rows:
            if ('unknown' in row['full_name'].lower() or row['full_name'] is None) and 'anonymous' in row['credit_line'].lower():
                writer.writerow(row)


if __name__ == '__main__':
    in_file = 'collection/cmoa.csv'
    out_file = 'data_from_code/unknown_by_anonymous.csv'
    data = get_unknown_by_anonymous(in_file)
    write_unknown_by_anonymous(out_file, data)
