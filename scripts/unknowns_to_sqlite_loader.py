#!usr/bin/env python3

import sqlite3
import csv
from collections import namedtuple

Data = namedtuple(
    'Data',
    ['headers', 'rows']
)


def prepare_csv_data(filename):
    with open(filename) as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')
        headers = tuple(next(reader))
        return Data(
            headers,
            [tuple(row) for row in reader]
        )


def write_data_to_sqlite(data, target_db):
    db = sqlite3.connect(target_db)
    cur = db.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS unknowns_from_anonymous {headers}'
        .format(headers=data.headers)
    )

    cur.executemany(
        'INSERT INTO unknowns_from_anonymous VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        data.rows
    )

    db.commit()
    db.close()


def run_the_jewels(filename, target_db):
    data = prepare_csv_data(filename)
    write_data_to_sqlite(data, target_db)


if __name__ == '__main__':
    filename = 'data_from_code/unknown_by_anonymous.csv'
    target_db = 'cmoa_unknowns.db'
    run_the_jewels(filename, target_db)
