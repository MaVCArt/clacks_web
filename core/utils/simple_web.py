import clacks

from clacks_web.core.http_handler import HTTPHandler
from clacks_web.core.html_marshaller import HTMLMarshaller


spec = {
    'interfaces': [
        'standard',
        'cmd_utils',
        'logging',
        'profiling',
        'web_core',
        'website_basic',
    ],
    'handlers': [],
    'adapters': [
        'header_kwargs',
        'cors',
        'gnu',
        'content_type'
    ]
}


# ----------------------------------------------------------------------------------------------------------------------
def simple_web_server(identifier, host, port, marshaller_type=HTMLMarshaller):
    server = clacks.ServerBase(identifier=identifier)

    # -- load a standard spec
    server.load_spec(spec)

    # -- give the user a single handler to work with, but don't start the server yet.
    server.register_handler(host, port, HTTPHandler(marshaller_type()))

    return server


# ----------------------------------------------------------------------------------------------------------------------
def simple_website(identifier, host, port, marshaller_type=HTMLMarshaller):
    server = clacks.ServerBase(identifier=identifier)

    # -- load a standard spec
    server.load_spec(spec)

    # -- give the user a single handler to work with, but don't start the server yet.
    server.register_handler(host, port, HTTPHandler(marshaller_type()))

    return server
