import clacks
from clacks_web import get


# ----------------------------------------------------------------------------------------------------------------------
class ClacksBasicRestAPIInterface(clacks.ServerInterface):

    _REQUIRED_INTERFACES = ['web_core']

    # ------------------------------------------------------------------------------------------------------------------
    @get('/', expose_as_method=False)
    def list_endpoints(self):
        result = dict()
        for method in self.server.resources:
            result[method] = sorted(list(set(self.server.resources[method].keys())))
        return result


clacks.register_server_interface_type('rest_basic', ClacksBasicRestAPIInterface)
