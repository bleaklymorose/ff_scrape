import sqlite3
from datetime import datetime


class AddToDB:

    def __init__(self, directory, players):
        self.directory = directory
        self.players = players
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M')

    @staticmethod
    def sanitize_input(sql_input):
        return ''.join(i for i in sql_input if str(sql_input).isalnum())

    def add_tables(self):
        for player in self.players:
            db_table = self.players[player]["fullNameDB"]
            self.sanitize_input(db_table)
            query = 'CREATE TABLE IF NOT EXISTS {}(datestamp TEXT, ' \
                    'count INTEGER, cum_sum INTEGER, common_count INTEGER, ' \
                    'frac_count INTEGER, tot_count INTEGER, tot_cum_sum INTEGER)'.format(db_table)
            self.c.execute(query)

    def add_tables_common(self):
        for player in self.players:
            db_table = self.players[player]["fullNameDB"]
            self.sanitize_input(db_table)
            query = 'CREATE TABLE IF NOT EXISTS {}(datestamp TEXT, ' \
                    'count INTEGER, sum INTEGER)'.format(db_table)
            self.c.execute(query)

    def data_entry(self):
        for player in self.players:
            query = 'INSERT INTO {0} VALUES("{1}", {2}, {3}, {4}, {5}, {6}, {7})'\
                .format(self.players[player]["fullNameDB"], self.time, self.players[player]["count"],
                        self.players[player]["sum"], self.players[player]["common_count"],
                        self.players[player]["frac_count"], self.players[player]["tot_count"],
                        self.players[player]["tot_sum"])
            self.c.execute(query)

    def data_entry_common(self):
        for player in self.players:
            query = 'INSERT INTO {0} VALUES("{1}", {2}, {3})'\
                .format(self.players[player]["fullNameDB"], self.time, self.players[player]["count"],
                        self.players[player]["sum"])
            self.c.execute(query)

    def poopy_butt_rodgers(self):
        for row in self.c.execute('SELECT * FROM {}'.format('aaronrodgers')):
            print(row)

    def __enter__(self):
        self.con = sqlite3.connect(self.directory)
        self.c = self.con.cursor()
        # returns the entire object using the 'with' 'as' syntax
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.con.commit()
        self.con.close()
