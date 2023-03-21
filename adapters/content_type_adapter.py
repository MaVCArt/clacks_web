import socket
from clacks.core.package import Package
from clacks import ServerAdapterBase, register_adapter_type


# ----------------------------------------------------------------------------------------------------------------------
class ContentTypeHeaderAdapter(ServerAdapterBase):

    # ------------------------------------------------------------------------------------------------------------------
    def server_post_digest(self, handler, connection, transaction_id, header_data, data, response):
        # type: (BaseRequestHandler, socket.socket, str, dict, dict, Response) -> None
        content_type = 'text/json'

        if 'Content-Type' in header_data:
            content_type = header_data['Content-Type']

        if 'content-type' in header_data:
            content_type = header_data['content-type']

        if 'Accept' in header_data:
            first_part = header_data['Accept'].split(',')[0]
            content_type = first_part

        response.header_data['Content-Type'] = content_type

    # ------------------------------------------------------------------------------------------------------------------
    def handler_pre_respond(self, connection, transaction_id, package):
        # type: (socket.socket, str, Package) -> None
        if 'header_data' not in package.payload:
            package.payload['header_data'] = dict()


register_adapter_type('content_type', ContentTypeHeaderAdapter)
