import os
import socket
from clacks.core.package import Package
from clacks import ServerAdapterBase, register_adapter_type


# ----------------------------------------------------------------------------------------------------------------------
class UserIdentityHeaderAdapter(ServerAdapterBase):

    # ------------------------------------------------------------------------------------------------------------------
    def handler_pre_respond(self, connection, transaction_id, package):
        # type: (socket.socket, str, Package) -> None
        if 'header_data' not in package.payload:
            package.payload['header_data'] = dict()

        package.header_data['Origin-Username'] = os.getenv('USERNAME')
        package.header_data['Origin-ComputerName'] = os.getenv('COMPUTERNAME')


register_adapter_type('user_identity', UserIdentityHeaderAdapter)
