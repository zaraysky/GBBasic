import re
import sys
from hw8.reports import ReportCSV, ReportJSON
# from reports import ReportCSV

from hw8.dataservice import SQLiteDataSource
# from dataservice import SQLiteDataSource


def print_help_and_exit():
    print('Формат запроса: export_openweather.py {--csv | --json | --html} filename [<город>]')
    sys.exit(1)


if len(sys.argv) < 3:
    print_help_and_exit()

_, output_format, file_name = sys.argv

if len(sys.argv) > 3:
    city = sys.argv[4]

if output_format not in ['--csv', '--json', '--html']:
    print_help_and_exit()

if not re.match(r'[\w\d]+\.?[\w\d]*', file_name):
    print_help_and_exit()

sq = SQLiteDataSource()
sq.setup('database.sqlite')
data = sq.load_data('weather')

if output_format == '--csv':
    rep = ReportCSV()
    res = rep.generate_report(data=data)

if output_format == '--json':
    rep = ReportJSON()
    res = rep.generate_report(data=data)


with open(file_name, 'w') as f:
    f.write(res)
