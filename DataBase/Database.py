import sqlite3


class DataBase:
    def __init__(self, connection_string):
        self.con = sqlite3.connect(connection_string)

    def insert_words(self, level_id, minuts, seconds):
        cur = self.con.cursor()
        cur.execute("""INSERT INTO all_information(level_id, minuts, seconds) VALUES(?, ?, ?)
        """, [level_id, minuts, seconds])
        self.con.commit()

    def all_words(self):
        cur = self.con.cursor()
        return cur.execute("""
                SELECT * FROM all_information
                """).fetchall()

    def get_music_volume(self):
        cur = self.con.cursor()
        result = cur.execute("""
                        SELECT volume FROM music_volume
                        WHERE id = 1
                        """).fetchone()
        return result

    def update_music_volume(self, volume):
        cur = self.con.cursor()
        cur.execute("""
                UPDATE music_volume
                SET volume = ?
                WHERE id = 1
                """, [volume]).fetchone()
        self.con.commit()

    def close(self):
        self.con.close()
