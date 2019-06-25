from utils import randomly_fill_weather_database


def main():
    print('Preparations...')
    n = int(input('How many cityes to download?'))
    print(n)
    if n < 50:
        randomly_fill_weather_database(n)
        print('Now run report service: export_openweather.py {--csv | --json | --html} filename [<город>]')
    else:
        print("Too much cities to parse")


if __name__ == '__main__':
    main()
