#!usr/bin/env python3

import sys
import csv
from collections import namedtuple, OrderedDict

Data = namedtuple(
    'Data',
    ['headers', 'rows']
)


def get_data(filename, has_headers=False):
    with open(filename) as f:
        reader = csv.DictReader(f)
        if has_headers:
            # separate headers and data to persist both for writing
            headers = reader.fieldnames
        else:
            # keep data types the same even if they're not present
            headers = OrderedDict()
        return Data(
            headers,
            list(reader)
        )


def find_unknown_by_anonymous(data):
    for row in data:
        if ('unknown' in row['full_name'].lower() or row['full_name'] is None) and 'anonymous' in row['credit_line'].lower():
            yield row


def write_unknown_by_anonymous(filename, data):
    if data.headers:
        writer = csv.DictWriter(open(filename, 'w'), fieldnames=data.headers)
        writer.writeheader()
    else:
        writer = csv.writer(open(filename, 'w'))

    rows = find_unknown_by_anonymous(data.rows)
    for row in rows:
        writer.writerow(row)


def run_the_jewels(infile, outfile, has_headers=False):
    data = get_data(infile, has_headers)
    write_unknown_by_anonymous(outfile, data)


if __name__ == '__main__':
    infile = 'collection/cmoa.csv'
    outfile = 'data_from_code/unknown_by_anonymous.csv'
    run_the_jewels(infile, outfile, True)
