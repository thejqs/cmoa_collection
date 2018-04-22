#!usr/bin/env python3

import sys
import sqlite3
import csv
from collections import namedtuple

Data = namedtuple(
    'Data',
    ['headers', 'rows']
)

Connection = namedtuple(
    'Connection',
    ['db', 'cur']
)


class SQLiteLoader:

    def __init__(self, infile, target_db):
        self.infile = infile
        self.db = target_db

    def prepare_csv_data(self, filename, has_headers=False):
        with open(filename) as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            if has_headers:
                headers = tuple(next(reader))
                # headers = None
            else:
                headers = tuple()

            return Data(
                headers,
                [tuple(row) for row in reader]
            )

    def connect_to_db(self, target_db):
        db = sqlite3.connect(target_db)
        return Connection(
            db,
            db.cursor()
        )

    def write_data_to_sqlite(self, data, headers, db_connection):
        try:
            db_connection.cur.execute(
                'CREATE TABLE IF NOT EXISTS unknowns_from_anonymous {headers}'
                .format(headers=headers)
            )
        except sqlite3.OperationalError:
            sys.exit('OH NO: No headers appear to be present for this dataset. No headers, no db table.')

        db_connection.cur.executemany(
            'INSERT INTO unknowns_from_anonymous VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            data
        )
        db_connection.db.commit()
        db_connection.db.close()

    def run_the_jewels(self, filename, target_db, has_headers):
        data = self.prepare_csv_data(filename, has_headers)
        if data.headers:
            connection = self.connect_to_db(target_db)
            self.write_data_to_sqlite(data.rows, data.headers, connection)
        else:
            sys.exit('YIKES: Not seeing any headers present. Without headers, we can\'t make a database table')


if __name__ == '__main__':
    filename = 'data_from_code/unknown_by_anonymous.csv'
    target_db = 'sqlite/cmoa_unknowns.db'
    loader = SQLiteLoader(filename, target_db)
    loader.run_the_jewels(loader.infile, loader.db, True)
