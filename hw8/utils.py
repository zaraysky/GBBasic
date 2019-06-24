import os
import json
import gzip
import time
import random
import sqlite3
import requests
from datetime import datetime

API_ID = '718de002422859ab14b955ef4fae4757'


def create_db():
    conn = sqlite3.connect("database.sqlite")  # или :memory: чтобы сохранить в RAM
    # conn = sqlite3.connect(":memory:")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    # Создание таблицы
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
      city_id integer(10) NOT NULL,
      city_name char(128) NOT NULL,
      data char(128) NOT NULL,
      temp float(128) NOT NULL,
      weather_id integer(10) NOT NULL
    );"""
    cursor.execute(create_script)

    return conn

def get_city_list():
    city_file = os.path.join(os.getcwd(), 'city.json')
    if not os.path.isfile(city_file):
        req = requests.get('http://bulk.openweathermap.org/sample/city.list.json.gz')
        gzipped_content = req.content
        print(gzipped_content[:10])
        decoded_content = gzip.decompress(gzipped_content).decode()
        with open(city_file, 'w') as f:
            f.write(decoded_content)


def get_weather_by_city_id_json(city_id):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'id': str(city_id), 'units': 'metric', 'appid': API_ID}
    req = requests.get(url, params=params)
    return json.loads(req.content.decode())


def fill_cities(conn):
    city_file = os.path.join(os.getcwd(), 'city.json')
    if not os.path.isfile(city_file):
        return False
    with open(city_file) as f:
        json_content = json.loads(f.read())

    cities_list = []
    for c in json_content:
        cities_list.append((c['id'], c['name'], c['country'], c['coord']['lat'], c['coord']['lon']))

    try:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO cities VALUES (?,?,?,?,?)", cities_list)
        conn.commit()
    except sqlite3.IntegrityError:
        print('Данные в cities уже есть')


def randomly_fill_weather_database(n=10):

    def get_country_list(conn):
        cursor = conn.cursor()
        res = cursor.execute('SELECT DISTINCT country FroM cities ORDER by country')
        return res.fetchall()

    def get_cities_list_by_country(conn, country):
        cursor = conn.cursor()
        res = cursor.execute('SelECT name from cities where country=? order by name', (country,))
        return res.fetchall()

    def get_city_id_by_country_and_name(conn, country, name):
        cursor = conn.cursor()
        print(country, name)
        res = cursor.execute('SelECT id from cities where country=? and name=? order by name', (country, name))
        return res.fetchall()

    get_city_list()
    conn = create_db()
    fill_cities(conn)
    countries = list(x[0] for x in get_country_list(conn))

    for _ in range(n):
        country = random.choice(countries)
        print(country)
        cities = get_cities_list_by_country(conn, country)
        city = random.choice(cities)[0]
        print(city)
        city_id = get_city_id_by_country_and_name(conn, country, city)[0][0]
        w = get_weather_by_city_id_json(city_id=city_id)
        time.sleep(random.random() + 1)
        temp = w['weather'][0]['id']
        weather_id = w['main']['temp']
        data = datetime.strftime(datetime.fromtimestamp(w['dt']), "%d/%m/%y %H:%M")

        cursor = conn.cursor()
        cursor.execute("INSERT INTO weather VALUES (?,?,?,?,?)", (int(city_id), city, data, float(temp), int(weather_id)))
        conn.commit()


# randomly_fill_weather_database()
