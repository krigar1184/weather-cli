import re
import json
import random

import pytest
import requests_mock

from weather import get_weather


def test_no_cities():
    assert get_weather() == 'Please provide at least one city name.'


@pytest.mark.parametrize(('cities', 'call_count'), [
    ((), 0),
    (('Bergen', 'Moscow', 'New York'), 6),
    (('Bergen', 'Bergen'), 2),
    (('Bergen', 'bergen'), 2),
    (('Bergen', 'bergen', 'BERGEN'), 2),
])
def test_api_calls_count(cities, call_count):
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text=json.dumps('[]'))
        m.get(
            re.compile(r'http://dataservice.accuweather.com/locations'),
            text=json.dumps([{'Key': random.randint(1000000, 2000000)}]),
        )
        get_weather(*cities)

        assert m.call_count == call_count
