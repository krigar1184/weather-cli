import re
import json
import random

import pytest
import requests_mock

from weather import get_weather, InvalidInputException


def test_no_cities():
    with pytest.raises(InvalidInputException):
        get_weather()


@pytest.mark.parametrize(('cities', 'expected'), [
    (('Bergen',), ['Bergen']),
    (('Bergen', 'bergen', 'BERGEN'), ['Bergen']),
])
def test_weather(cities, expected):
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
        results = get_weather(*cities)['results']

    assert sorted(results.keys()) == sorted(['country', 'city', 'region', 'temperature'])
