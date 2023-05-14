import clacks
import requests
import unittest
import clacks_web


# ----------------------------------------------------------------------------------------------------------------------
def test_decorator(fn):
    def wrapper(*args, **kwargs):
        return 'foobar'
    return wrapper


# ----------------------------------------------------------------------------------------------------------------------
class DecoratorTestInterface(clacks.ServerInterface):

    # ------------------------------------------------------------------------------------------------------------------
    @clacks_web.post('/test_result')
    @test_decorator
    def test_result(self, *args, **kwargs):
        return 'hello world - this should not be the result!'


clacks.register_server_interface_type('decorator_test', DecoratorTestInterface)


# ----------------------------------------------------------------------------------------------------------------------
class TestWebCommandDecorators(unittest.TestCase):

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def create_server(cls):
        api = clacks_web.simple_rest_api(identifier='testing', host='localhost', port=6000)
        api.register_interface_by_key(interface_type='decorator_test')
        return api

    # ------------------------------------------------------------------------------------------------------------------
    def test_result_proc(self):
        server = self.create_server()
        server.start(blocking=False)

        result = requests.post(
            'http://localhost:6000/test_result',
            json={'foo': 'This should be changed!'}
        )

        result.raise_for_status()

        result = result.json()['response']

        server.end()

        if result != 'foobar':
            self.fail('Result processor did not fire!')
