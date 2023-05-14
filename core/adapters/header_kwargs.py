import socket
from clacks.core.package import Package
from clacks.core.handler import BaseRequestHandler
from clacks import ServerAdapterBase, register_adapter_type


# ----------------------------------------------------------------------------------------------------------------------
class HeaderKwargAdapter(ServerAdapterBase):
    """
    "Header kwargs" adapter. Used in web servers, as arguments provided to HTTP requests are passed in the header data,
    not the body.

    This method basically moves any such keyword arguments to the kwargs dict in the data package, thereby making it so
    that rather than account for this behaviour in the ServerCommand class, we can just create an adapter for it, which
    is then only used for web servers.

    This makes the web-server behaviour nice and separated.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def marshaller_pre_encode_package(self, server, handler, marshaller, transaction_id, package):
        if 'args' in package.payload:
            if package.payload['args']:
                raise ValueError(
                    'In use cases where we get keyword arguments from headers, positionals are not supported!'
                )
            del package.payload['args']

        if 'kwargs' not in package.payload:
            return

        for key, value in package.payload['kwargs']:
            package.payload[key] = value

        del package.payload['kwargs']

    # ------------------------------------------------------------------------------------------------------------------
    def server_pre_digest(self, server, handler, connection, transaction_id, header_data, data):
        # -- in this instance, assuming data comes from the header, all data in the body is considered a keyword arg.
        data.update(kwargs=data.copy())

        for k in data['kwargs']:
            if k == 'kwargs':
                continue
            del data[k]

        for key, arg in header_data.get('kwargs', dict()).items():
            data['kwargs'][key] = arg

        if 'kwargs' in header_data:
            del header_data['kwargs']

        if 'command' in header_data:
            data['command'] = header_data.get('command')
            del header_data['command']


register_adapter_type('header_kwargs', HeaderKwargAdapter)
