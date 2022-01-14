import sqlite3


class DataBase:
    def __init__(self, connection_string):
        self.con = sqlite3.connect(connection_string)

    def best_time(self):
        cur = self.con.cursor()
        # словарь с уровнями и значениями лучшего времени
        best_times_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        # проходимся по всем значениям
        for i in range(1, 7):
            # берем результаты с одного уровня
            values = cur.execute("""
                SELECT * FROM all_information
                WHERE level_id == ?
                """, [i]).fetchall()
            # усли результатов нет, то ничего не добавляем
            if len(values) == 0:
                pass
            # если есть значения времени
            else:
                # проходимся по всем значениям и выбираем максимальное время
                max_minuts = 0
                max_sec = 0
                for el in values:
                    if el[2] > max_minuts:
                        max_minuts = el[2]
                        max_sec = el[3]
                    elif el[2] == max_minuts and el[3] > max_sec:
                        max_minuts = el[2]
                        max_sec = el[3]
                best_times_dict[i].append([max_minuts, max_sec])
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
