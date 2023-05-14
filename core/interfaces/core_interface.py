import clacks
import inspect
from clacks import command


# ----------------------------------------------------------------------------------------------------------------------
class ClacksCoreWebAPIInterface(clacks.ServerInterface):
    """
    Core Web API Interface - this registers all methods necessary to create a web-based REST API for your server.
    This is not dependent on an HTTP handler, but for a server to function like a true REST API, it will need an HTTP
    Handler with a JSON Marshaller (generally, since JSON is the most common interchange format).

    If used in a REST interface setup, the assumption is made that the developer is using a set of decorators designed
    for that purpose. `clacks_web.decorators` includes these decorators: post, get, put, patch, delete, etc...
    """

    # -- this interface requires the "status_code" adapter to function, as it transmutes our results from a tuple
    # -- into a value and a code.
    _REQUIRED_ADAPTERS = ['status_code', 'header_data_as_kwarg']

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        super(ClacksCoreWebAPIInterface, self).__init__()
        self.resources = dict()

    # ------------------------------------------------------------------------------------------------------------------
    def get_resources_from_object(self, obj):
        """
        From a given object, register all callables as resources on the server.

        :param obj: the object to gather resources from. Usually a ServerInterface instance.
        :type obj: object

        :return: None
        :rtype: NoneType
        """
        for k in dir(obj):
            v = getattr(obj, k)

            if not callable(v):
                continue

            if not inspect.ismethod(v):
                continue

            # -- don't register private methods as resources, but register decorated hidden ones.
            if hasattr(v, 'private'):
                if v.private:
                    continue

            if v.__name__.startswith('_'):
                continue

            resource_type = 'GET'
            path = '/{name}'.format(name=v.__name__)

            if hasattr(v, 'resource_type'):
                resource_type = v.resource_type

            if hasattr(v, 'path'):
                path = v.path

            # -- construct a ServerCommand instance, this will retain all decorators.
            resource = command.command_from_callable(self, v, cls=clacks.ServerCommand)

            if not resource:
                continue

            self.register_resource(resource_type, path, resource)

    # ------------------------------------------------------------------------------------------------------------------
    def _initialize(self, parent):
        success = super(ClacksCoreWebAPIInterface, self)._initialize(parent)

        if not success:
            return False

        for _, interface in self.server.interfaces.items():
            self.get_resources_from_object(interface)

        if not self.resources:
            raise ValueError('No resources registered - please register at least one REST resource!')

        return True

    # ------------------------------------------------------------------------------------------------------------------
    def register_resource(self, resource_type, path, func):
        """
        Register a resource to this interface, allowing for it to be requested through the standard methods.
        This is how a resource becomes discoverable through HTTP methods like GET, POST, PUT etc.

        :param resource_type: Name of the method to use to request this resource. For example, GET, POST, etc...
        :type resource_type: str

        :param path: The path at which to register the resource. Example: '/list_methods'
        :type path: str

        :param func: callable function to register at the given resource.
        :type func: callable

        """
        if resource_type not in self.resources:
            self.resources[resource_type] = dict()
        self.logger.debug('Registering REST resource %s of type %s at path %s' % (func, resource_type, path))
        self.resources[resource_type][path] = func

    # ------------------------------------------------------------------------------------------------------------------
    def get_resource(self, resource_type, path):
        """
        Get a registered resource by its type and path.

        :param resource_type: Name of the method to use to request this resource. For example, GET, POST, etc...
        :type resource_type: str

        :param path: The path at which to register the resource. Example: '/list_methods'
        :type path: str

        :return: The resource, if one was found. None otherwise.
        :rtype: object(callable)
        """
        if resource_type not in self.resources:
            msg = f'Resource type {resource_type} is not recognized!'
            self.logger.error(msg)
            raise clacks.errors.ClacksCommandNotFoundError(msg)

        if path not in self.resources[resource_type]:
            msg = f'Resource {path} of type {resource_type} could not be found!'
            self.logger.error(msg)
            raise clacks.errors.ClacksCommandNotFoundError(msg)

        return self.resources[resource_type][path]

    # ------------------------------------------------------------------------------------------------------------------
    def _method(self, method, *args, **kwargs):
        path = kwargs.get('path')

        if '_header_data' in kwargs:
            path = kwargs['_header_data'].get('path')
            del kwargs['_header_data']

        if not path:
            raise clacks.errors.ClacksBadCommandArgsError('No "path" argument provided in kwargs!')

        resource = self.get_resource(method, path)

        return resource(*args, **kwargs), clacks.ReturnCodes.OK

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.returns_status_code
    @clacks.takes_header_data
    def POST(self, *args, **kwargs):
        """
        Catch-all POST method, receives POST requests and forwards them to the _method private method. Will return the
        result of whatever method is retrieved by the given resource path.

        :return: Whatever the result of the call is
        """
        return self._method('POST', *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.returns_status_code
    @clacks.takes_header_data
    def GET(self, *args, **kwargs):
        """
        Catch-all GET method, receives GET requests and forwards them to the _method private method. Will return the
        result of whatever method is retrieved by the given resource path.

        :return: Whatever the result of the call is
        """
        return self._method('GET', *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.returns_status_code
    @clacks.takes_header_data
    def PUT(self, *args, **kwargs):
        """
        Catch-all PUT method, receives PUT requests and forwards them to the _method private method. Will return the
        result of whatever method is retrieved by the given resource path.

        :return: Whatever the result of the call is
        """
        return self._method('PUT', *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.returns_status_code
    @clacks.takes_header_data
    def PATCH(self, *args, **kwargs):
        """
        Catch-all PATCH method, receives PATCH requests and forwards them to the _method private method. Will return the
        result of whatever method is retrieved by the given resource path.

        :return: Whatever the result of the call is
        """
        return self._method('PATCH', *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.returns_status_code
    @clacks.takes_header_data
    def DELETE(self, *args, **kwargs):
        """
        Catch-all DELETE method, receives DELETE requests and forwards them to the _method private method.
        Will return the result of whatever method is retrieved by the given resource path.

        :return: Whatever the result of the call is
        """
        return self._method('DELETE', *args, **kwargs)


clacks.register_server_interface_type('web_core', ClacksCoreWebAPIInterface)
