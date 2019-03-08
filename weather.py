#!/usr/bin/env python

import os
import sys
from collections import defaultdict
import json

import requests


API_KEY = os.environ.get('WEATHER_API_KEY')


def get_weather(*cities):
    if not cities:
        return 'Please provide at least one city name.'

    cities = set([x.lower() for x in cities])
    result = defaultdict(list)
    location_keys = _get_location_keys(*cities)

    return _get_forecasts(**location_keys)


def _get_location_keys(*cities):
    result = {}
    url_template = f'http://dataservice.accuweather.com/locations/v1/cities/search'\
                   f'?apikey={API_KEY}&q={{city}}'

    with requests.Session() as session:
        for city in cities:
            api_response = _make_api_request(session, url_template.format(city=city))

            if api_response.status_code != 200:
                continue  # TODO handle error

            json_response = json.loads(api_response.text)
            result[city] = [x['Key'] for x in json_response]

    return result


def _get_forecasts(**location_keys):
    url_template = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{key}'\
                   f'?apikey={API_KEY}'
    result = defaultdict(list)

    with requests.Session() as session:
        for city, keys in location_keys.items():
            for key in keys:
                api_response = _make_api_request(session, url_template.format(key=key))

                if api_response.status_code != 200:
                    continue  # TODO handle error

                json_response = json.loads(api_response.text)
                result[city].append(json_response)

        return result


def _make_api_request(session, url, **query_params):
    return requests.get(url.format(apikey=API_KEY))


if __name__ == '__main__':
    cities = sys.argv[1:]
    print(get_weather(*cities))
