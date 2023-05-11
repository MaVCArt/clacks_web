import socket
from clacks.core.package import Package
from clacks import ServerAdapterBase, register_adapter_type


# ----------------------------------------------------------------------------------------------------------------------
class FirefoxHeaderAdapter(ServerAdapterBase):

    # ------------------------------------------------------------------------------------------------------------------
    def handler_pre_respond(self, server, handler, connection, transaction_id, package):
        if 'header_data' not in package.payload:
            package.payload['header_data'] = dict()
        package.header_data['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'


register_adapter_type('firefox', FirefoxHeaderAdapter)
