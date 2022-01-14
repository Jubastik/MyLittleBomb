import sqlite3


class DataBase:
    def __init__(self, connection_string):
        self.con = sqlite3.connect(connection_string)

    def get_best_time(self):
        cur = self.con.cursor()
        # словарь с уровнями и значениями лучшего времени
        best_times_dict = {}
        # проходимся по всем значениям
        values = cur.execute("""
            SELECT l.level_name, a.minuts, a.seconds FROM all_information a
            join levels l on a.level_id = l.id
            """).fetchall()
        # проходимся по всем значениям и выбираем максимальное время
        for v in values:
            if v[0] not in best_times_dict:
                best_times_dict[v[0]] = [v[1], v[2]]
            else:
                if v[1] < best_times_dict[v[0]][0]:
                    best_times_dict[v[0]] = [v[1], v[2]]
                elif v[1] == best_times_dict[v[0]][0] and v[2] < best_times_dict[v[0]][1]:
                    best_times_dict[v[0]] = [v[1], v[2]]
        return best_times_dict

    def insert_words(self, level_id, minuts, seconds):
        cur = self.con.cursor()
        if level_id == 'own':
            level_id = 6
        cur.execute("""INSERT INTO all_information(level_id, minuts, seconds) VALUES(?, ?, ?)
                """, [level_id, minuts, seconds])
        self.con.commit()

    def all_inf(self):
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
