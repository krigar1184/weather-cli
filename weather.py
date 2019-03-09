#!/usr/bin/env python3


import sys
from pprint import pprint

from src import get_weather


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.stderr.write('Not enough arguments\n')
        sys.exit(1)

    city, *_ = sys.argv[1:]

    try:
        pprint(get_weather(city))
    except Exception:
        e, info = sys.exc_info()
        sys.stderr.write(f'''Error occurred: {e}
            {info}
        ''')
        sys.exit(1)
