import sqlite3


class DataBase:
    def __init__(self, connection_string):
        self.con = sqlite3.connect(connection_string)

    def insert_words(self, level_id, minuts, seconds):
        cur = self.con.cursor()
        cur.execute("""INSERT INTO all_information(level_id, minuts, seconds) VALUES(?, ?, ?)
        """, [level_id, minuts, seconds])
        self.con.commit()

    def close(self):
        self.con.close()

    def all_words(self):
        cur = self.con.cursor()
        return cur.execute("""
        SELECT * FROM all_information
        """).fetchall()
