import clacks
import requests
import unittest
import clacks_web


# ----------------------------------------------------------------------------------------------------------------------
def arg_proc(server_command, *args, **kwargs):
    kwargs['foo'] = 'bar'
    return args, kwargs


# ----------------------------------------------------------------------------------------------------------------------
def result_proc(server_command, result):
    return 'foobar'


# ----------------------------------------------------------------------------------------------------------------------
class DecoratorTestInterface(clacks.ServerInterface):

    # ------------------------------------------------------------------------------------------------------------------
    @clacks_web.post('/test_result')
    @clacks.decorators.process_result([result_proc])
    def test_result(self, *args, **kwargs):
        return 'hello world - this should not be the result!'

    # ------------------------------------------------------------------------------------------------------------------
    @clacks_web.post('/test_args')
    @clacks.decorators.process_arguments([arg_proc])
    def test_args(self, *args, **kwargs):
        return kwargs.get('foo') == 'bar'


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
    def test_arg_proc(self):
        server = self.create_server()
        server.start(blocking=False)

        result = requests.post(
            'http://localhost:6000/test_args',
            json={'foo': 'This should be changed!'}
        ).json()['response']

        if result is not True:
            self.fail('Arg processor did not fire!')

        server.end()

    # ------------------------------------------------------------------------------------------------------------------
    def test_result_proc(self):
        server = self.create_server()
        server.start(blocking=False)

        result = requests.post(
            'http://localhost:6000/test_result',
            json={'foo': 'This should be changed!'}
        ).json()['response']

        if result != 'foobar':
            self.fail('Result processor did not fire!')

        server.end()
