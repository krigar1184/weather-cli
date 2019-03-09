import os
import json
from http import HTTPStatus

import requests


API_KEY = os.environ.get('WEATHER_API_KEY')


class APIException(Exception):
    pass


def get_weather(city):
    city = city.capitalize()
    weather = _get_current_weather(city)
    result = {'results': []}

    for city, item in weather.items():
        result['results'] = {
            'country': item['location']['country'],
            'city': city,
            'region': item['location']['region'],
            'temperature': item['current']['temp_c'],
        }

    return result


def _get_current_weather(city):
    url_template = f'http://api.apixu.com/v1/current.json?key={API_KEY}&q={{}}'
    api_response = _make_api_request(url_template.format(city))

    if api_response.status_code != HTTPStatus.OK:
        raise APIException(f'''Failed to fetch location key for {city}
            Response {api_response.status_code}
            {api_response.text}''')

    json_response = json.loads(api_response.text)

    return {city: json_response}


def _make_api_request(url, **query_params):
    return requests.get(url.format(apikey=API_KEY))
