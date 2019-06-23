import os
import re
import sys
import json
import gzip
import pprint
import requests
import sqlite3

API_ID = '718de002422859ab14b955ef4fae4757'

def print_help_and_exit():
    print('Формат запроса: export_openweather.py {--csv | --json | --html} filename [<город>]')
    sys.exit(1)

if len(sys.argv) < 4:
    print_help_and_exit()
else:
    print('Число параметров адекватное')

_, output_format, file_name, city = sys.argv

if output_format not in ['--csv', '--json', '--html']:
    print_help_and_exit()
else:
    print(f"Формат задан верно: {output_format}")

if not re.match(r'[\w\d]+\.?[\w\d]*', file_name):
    print_help_and_exit()
else:
    print(f"Имя файла задано правильно: {file_name}")

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
    params = {'id': str(city_id), 'appid': API_ID}
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
    res = cursor.execute('SelECT id from cities where country=? and name=? order by name', (country, name))
    return res.fetchall()


# get_city_list()

conn = create_db()
#
# fill_cities(conn)

# pprint.pprint(get_weather_by_city_id_json(2172797))
countries = list(x[0] for x in get_country_list(conn))
print('Вот список стран:')
print(' '.join(countries))

country = input('Введите двузначный код страны').upper()[:2]

if country not in countries:
    print('Нет такой страны')
    sys.exit()

cities = list(x[0] for x in get_cities_list_by_country(conn, country))
if len(cities) > 20:
    print("Список городов слишком длинный")
else:
    print(cities)
