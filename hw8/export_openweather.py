import re
import sys
from reports import ReportCSV, ReportJSON, ReportHTML
from dataservice import SQLiteDataSource


def print_help_and_exit():
    print('Request format is  запроса: export_openweather.py {--csv | --json | --html} filename [<город>]')
    sys.exit(1)


if len(sys.argv) < 3:
    print_help_and_exit()

_, output_format, file_name = sys.argv[:3]

city = None
if len(sys.argv) > 3:
    city = sys.argv[3]

if output_format not in ['--csv', '--json', '--html']:
    print_help_and_exit()

if not re.match(r'[\w\d]+\.?[\w\d]*', file_name):
    print_help_and_exit()

sq = SQLiteDataSource()
sq.setup('database.sqlite')
if city is None:
    data = sq.load_data('weather')
else:
    data = sq.filter_data('weather', 'city_name', city)

if output_format == '--csv':
    rep = ReportCSV()
    res = rep.generate_report(data=data)

if output_format == '--json':
    rep = ReportJSON()
    res = rep.generate_report(data=data)

if output_format == '--html':
    rep = ReportHTML()
    res = rep.generate_report(data=data)


with open(file_name, 'w') as f:
    f.write(res)
