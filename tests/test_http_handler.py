import clacks
import requests
import unittest
import clacks_web


# ----------------------------------------------------------------------------------------------------------------------
class TestHTTPHandler(unittest.TestCase):

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def create_handler(cls):
        handler = clacks_web.HTTPHandler(clacks.JSONMarshaller())
        return handler

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def create_server(cls):
        server = clacks.ServerBase(identifier='UNITTEST SERVER', start_queue=False)
        server.register_interface_by_key('standard')
        interface = server.interfaces.get('standard')

        def _list_commands(*args, **kwargs):
            return list(server.commands.keys())

        server.register_command('LIST_COMMANDS', clacks.command_from_callable(interface, _list_commands))
        server.register_adapter('header_kwargs', clacks_web.HeaderKwargAdapter())
        return server

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def create_proxy(cls, server):
        address = server.socket_addresses[0]
        handler = cls.create_handler()

        proxy = clacks.ClientProxyBase(address, handler, connect=False)
        proxy.register_interface_by_type('standard')

        proxy.register_adapter(clacks_web.HeaderKwargAdapter())
        proxy.connect()
        return proxy

    # ------------------------------------------------------------------------------------------------------------------
    def test_register_handler(self):
        server = self.create_server()

        assert len(server.sockets) == 0

        handler = self.create_handler()
        server.register_handler(host='localhost', port=clacks.get_new_port('localhost'), handler=handler)

        assert len(server.sockets) == 1

        # -- start the server, this should create a handler thread.
        server.start()

        assert len(server.handler_threads) == 1

    # ------------------------------------------------------------------------------------------------------------------
    def test_connect_client(self):
        server = self.create_server()
        host, port = 'localhost', clacks.get_new_port('localhost')
        server.register_handler(host, port, handler=self.create_handler())
        server.start()
        client = self.create_proxy(server)

    # ------------------------------------------------------------------------------------------------------------------
    def test_requests(self):
        server = self.create_server()

        host, port = 'localhost', clacks.get_new_port('localhost')
        server.register_handler(host, port, handler=self.create_handler())
        server.start()

        response = requests.request('list_commands', 'http://%s:%s' % ('localhost', port))

        # -- make sure the content is decoded correctly
        _ = response.json()

        response.raise_for_status()
