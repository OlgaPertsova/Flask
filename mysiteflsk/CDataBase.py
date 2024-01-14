import math
import time
import sqlite3


class CDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = "SELECT * FROM mymenu"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except IOError:
            print("Ошибка чтения из БД")
        return []

    def cours(self, title, text, url):
        try:
            self.__cur.execute("SELECT COUNT() as 'count' FROM cours WHERE url LIKE ?", (url,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Курс с таким url уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO cours VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления курса в бд", e)
            return False

        return True

    def get_cours_anonce(self):
        try:
            self.__cur.execute("SELECT id, title, text, url FROM cours ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения курса из бд:", e)

        return []