import clacks

from . import HTTPHandler
from . import HeaderKwargAdapter
from . import CORSHeaderAdapter


# ----------------------------------------------------------------------------------------------------------------------
def simple_rest_api(identifier, host, port):
    server = clacks.ServerBase(identifier=identifier)
    return simple_rest_api_from_server(server, host, port)


# ----------------------------------------------------------------------------------------------------------------------
def simple_rest_api_from_server(server, host, port):
    # -- register a standard set of interfaces for basic out-of-the-box functionality
    server.register_interface_by_key('standard')
    server.register_interface_by_key('cmd_utils')
    server.register_interface_by_key('logging')
    server.register_interface_by_key('profiling')
    server.register_interface_by_key('web_core')
    server.register_interface_by_key('rest_basic')

    # -- give the user a single handler to work with, but don't start the server yet.
    server.register_handler(host, port, HTTPHandler(clacks.JSONMarshaller()))

    # -- as this is a web server, we need a header kwarg adapter, or standard REST requests won't work for it.
    server.register_adapter('header_kwargs', HeaderKwargAdapter())
    server.register_adapter('cors', CORSHeaderAdapter())

    return server
