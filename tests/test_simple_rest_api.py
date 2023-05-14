import time
import requests
import unittest
import clacks_web


# ----------------------------------------------------------------------------------------------------------------------
class TestSimpleRestAPI(unittest.TestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test_simple_get(self):
        api = clacks_web.simple_rest_api(identifier='testing', host='localhost', port=6000)
        api.start(blocking=False)

        time.sleep(1)

        response = requests.get('http://localhost:6000/')
        response.raise_for_status()

        a = response.json()['response']


        b = dict()
        for method in api.resources:
            b[method] = sorted(list(set(api.resources[method].keys())))

        assert a == b

        api.end()

    # ------------------------------------------------------------------------------------------------------------------
    def test_simple_rest_api(self):
        _ = clacks_web.simple_rest_api(identifier='testing', host='localhost', port=6001)
