#!/usr/bin/env python

import os
import sys
from collections import defaultdict
import json
from pprint import pprint
from http import HTTPStatus

import requests


API_KEY = os.environ.get('WEATHER_API_KEY')


class APIException(Exception):
    pass


class InvalidInputException(Exception):
    pass


def get_weather(*cities):
    if not cities:
        raise InvalidInputException('Please provide at least one city name.')

    cities = set([x.capitalize() for x in cities])
    weather = _get_current_weather(*cities)
    result = {'results': []}

    for city, data in weather.items():
        for item in data:
            result['results'] = {
                'country': item['location']['country'],
                'city': city,
                'region': item['location']['region'],
                'temperature': item['current']['temp_c'],
            }

    return result


def _get_current_weather(*cities):
    url_template = f'http://api.apixu.com/v1/current.json?key={API_KEY}&q={{}}'
    result = defaultdict(list)

    with requests.Session() as session:
        for city in cities:
            api_response = _make_api_request(session, url_template.format(city))

            if api_response.status_code != HTTPStatus.OK:
                raise APIException(f'''Failed to fetch location key for {city}
                    Response {api_response.status_code}
                    {api_response.text}''')

            json_response = json.loads(api_response.text)
            result[city].append(json_response)

        return result


def _make_api_request(session, url, **query_params):
    return requests.get(url.format(apikey=API_KEY))


if __name__ == '__main__':
    cities = sys.argv[1:]

    try:
        pprint(get_weather(*cities))
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)
