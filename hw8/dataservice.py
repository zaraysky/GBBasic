import sqlite3
import json

from abc import ABC, abstractmethod


class DataSource(ABC):
    def __init__(self):
        self.conn = None

    @abstractmethod
    def setup(self, database_name):
        raise NotImplementedError

    @abstractmethod
    def load_data(self, data):
        raise NotImplementedError


# noinspection SqlNoDataSourceInspection
class SQLiteDataSource(DataSource):
    def __init__(self):
        super().__init__()
        self.conn = None

    def setup(self, database_name):
        database_name = database_name or ':memory:'  # :memory: чтобы сохранить в RAM
        self.conn = sqlite3.connect(database_name)

    def load_data(self, table_name):
        if self.conn is None:
            print("Соединение с базой не установлено")
            return

        res = None
        try:
            cursor = self.conn.cursor()
            res = cursor.execute(f"SELECT * FROM {table_name}")
        except sqlite3.IntegrityError:
            print(f'Ошибка записи')

        return res.fetchall()


if __name__ == '__main__':
    sq = SQLiteDataSource()
    sq.setup('database.sqlite')
    print(sq.load_data('weather'))
