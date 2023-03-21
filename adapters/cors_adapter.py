import socket
from clacks.core.package import Package
from clacks import ServerAdapterBase, register_adapter_type


# ----------------------------------------------------------------------------------------------------------------------
class CORSHeaderAdapter(ServerAdapterBase):

    # ------------------------------------------------------------------------------------------------------------------
    def handler_pre_respond(self, connection, transaction_id, package):
        # type: (socket.socket, str, Package) -> None
        if 'header_data' not in package.payload:
            package.payload['header_data'] = dict()
        package.header_data['Access-Control-Allow-Origin'] = '*'
        package.header_data['Access-Control-Allow-Headers'] = '*'
        package.header_data['Access-Control-Allow-Methods'] = '*'


register_adapter_type('cors', CORSHeaderAdapter)
