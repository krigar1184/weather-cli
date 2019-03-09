import json
import random

import pytest
import requests_mock

from src import get_weather, APIException


@pytest.mark.parametrize(('city', 'expected'), [
    ('Bergen', ['Bergen']),
])
def test_weather(city, expected):
    def text_callback(request, context):
        return json.dumps({
            'current': {'temp_c': random.randint(-30, 30)},
            'location': {
                'country': '',
                'name': '',
                'region': None,
            },
        })

    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text=text_callback)
        results = get_weather(city)['results']

    assert sorted(results.keys()) == sorted(['country', 'city', 'region', 'temperature'])


def test_nonexistent_city():
    with requests_mock.mock() as m, pytest.raises(APIException):
        m.get(requests_mock.ANY, status_code=400)
        get_weather('idontexist')
