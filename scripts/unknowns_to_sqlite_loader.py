#!usr/bin/env python3

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

    def __init__(self, infile, target_db, tablename):
        self.infile = infile
        self.db = target_db
        self.tablename = tablename
        self.__missing_db_error = 'OH JEEZ: Seems like the target_db parameter isn\'t set correctly. Without those, we can\'t make a database table.'
        self.__missing_db_params_error = 'GOLLY: Not seeing either headers or a tablename present. Without those, we can\'t make a database table.'

        if not self.tablename or not self.db:
            raise Exception(self.__missing_db_error)

    def prepare_csv_data(self, filename, has_headers=False):
        with open(filename) as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            if has_headers:
                headers = tuple(next(reader))
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

    def load_data(self, data, headers, tablename, db_connection):
        try:
            db_connection.cur.execute(
                'CREATE TABLE IF NOT EXISTS {tablename} {headers}'
                .format(tablename=tablename, headers=headers)
            )
        except sqlite3.OperationalError:
            raise Exception(self.__missing_db_params_error)

        header_count = len(headers)
        sql = 'INSERT INTO {tablename} VALUES('.format(tablename=tablename) + ','.join(header_count * ['?']) + ')'
        db_connection.cur.executemany(sql, data)
        db_connection.db.commit()
        db_connection.db.close()

    def run_the_jewels(self, filename, target_db, tablename):
        data = self.prepare_csv_data(filename, has_headers)
        if data.headers and tablename:
            connection = self.connect_to_db(target_db)
            self.load_data(data.rows, data.headers, tablename, connection)
        else:
            raise Exception(self.__missing_db_params_error)


if __name__ == '__main__':
    filename = 'data_from_code/unknown_by_anonymous.csv'
    target_db = 'sqlite/cmoa_unknowns.db'
    tablename = 'unknowns_from_anonymous'
    loader = SQLiteLoader(filename, target_db, tablename)
    loader.run_the_jewels(loader.infile, loader.db, loader.tablename)
