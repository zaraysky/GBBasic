import sys
from .utils import randomly_fill_weather_database


def main():
    print('Preparations...')
    randomly_fill_weather_database(20)

    # print('I\'m main')
    # print(':'.join(sys.argv))


if __name__ == '__main__':
    main()
