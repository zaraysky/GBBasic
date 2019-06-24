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
    def save_data(self, data, dest):
        raise NotImplementedError


class DataService():
    def __init__(self):
        self.datasource = None

    def add_data_source(self, ds: DataSource):
        self.datasource = ds

    def save_data(self, data, dest):
        self.datasource.save_data(data=data, dest=dest)


# noinspection SqlNoDataSourceInspection
class SQLiteDataSource(DataSource):
    def __init__(self):
        super().__init__()
        self.conn = None

    def setup(self, database_name):
        database_name = database_name or ':memory:'  # :memory: чтобы сохранить в RAM
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # Создание таблиц
        create_script = """
        CREATE TABLE IF NOT EXISTS cities (
          id integer(10) PRIMARY KEY NOT NULL,
          name char(128) NOT NULL,
          country char(128) NOT NULL,
          lat float(128) NOT NULL,
          lon float(128) NOT NULL
        );"""
        cursor.execute(create_script)

        create_script = """
        CREATE TABLE IF NOT EXISTS weather (
          id integer(10) PRIMARY KEY NOT NULL,
          name char(128) NOT NULL,
          country char(128) NOT NULL,
          lat float(128) NOT NULL,
          lon float(128) NOT NULL
        );"""
        cursor.execute(create_script)

        self.conn = conn

    def save_data(self, data, dest):
        if self.conn is None:
            print("Соединение с базой не установлено")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO {dest} VALUES {tuple(data)}")
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f'Ошибка записи')


if __name__ == '__main__':
    sq = SQLiteDataSource()
    sq.setup('mydata')
    sq.save_data([1, 'xxx', 'RU', 12, 13], 'cities', )
