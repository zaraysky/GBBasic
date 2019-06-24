import re
import sys
from .reports import ReportCSV

def print_help_and_exit():
    print('Формат запроса: export_openweather.py {--csv | --json | --html} filename [<город>]')
    sys.exit(1)


if len(sys.argv) < 4:
    print_help_and_exit()

_, output_format, file_name, city = sys.argv

if output_format not in ['--csv', '--json', '--html']:
    print_help_and_exit()

if not re.match(r'[\w\d]+\.?[\w\d]*', file_name):
    print_help_and_exit()

