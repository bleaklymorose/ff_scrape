import sqlite3
from datetime import datetime


class DataBase:

    def __init__(self, database):

        self.database = database

    def __enter__(self):

        self.con = sqlite3.connect(self.database)
        self.c = self.con.cursor()
        return self.c

    def __exit__(self, exception_type, exception_value, traceback):

        self.con.commit()
        self.con.close()


class AddToDB:

    def __init__(self, cursor, players):

        self.database = cursor
        self.players = players

    @staticmethod
    def sanitize_input(sql_input):

        return ''.join(i for i in sql_input if str(sql_input).isalnum())

    def add_tables(self):

        for player in self.players:
            db_table = self.players[player]["fullNameDB"]
            self.sanitize_input(db_table)
            query = 'CREATE TABLE IF NOT EXISTS {}(datestamp TEXT, ' \
                    'count INTEGER)'.format(db_table)

            self.database.execute(query)

    def data_entry(self):

        for player in self.players:
            db_table = self.players[player]["fullNameDB"]
            db_table_count = self.players[player]["count"]
            query = 'INSERT INTO {0} VALUES("{1}", {2})'.format(db_table, datetime.now(), db_table_count)
            self.database.execute(query)

    def poopy_butt_rodgers(self):

        for row in self.database.execute('SELECT * FROM {}'.format('aaronrodgers')):
            print(row)

