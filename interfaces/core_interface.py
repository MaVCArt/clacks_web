import clacks
import inspect
from clacks import ServerCommand


# ----------------------------------------------------------------------------------------------------------------------
class ClacksCoreWebAPIInterface(clacks.ServerInterface):
    """
    Core Web API Interface - this registers all methods necessary to create a web-based REST API for your server.
    This is not dependent on an HTTP handler, but for a server to function like a true REST API, it will need an HTTP
    Handler with a JSON Marshaller (generally, since JSON is the most common interchange format).

    If used in a REST interface setup, the assumption is made that the developer is using a set of decorators designed
    for that purpose. `clacks_web.decorators` includes these decorators: post, get, put, patch, delete, etc...
    """

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
            resource = ServerCommand.construct(self, v)
            if not resource:
                continue

            self.register_resource(resource_type, path, resource)

    # ------------------------------------------------------------------------------------------------------------------
    def _initialize(self):
        # type: () -> bool
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

        :return: None
        :rtype: None
        """
        if resource_type not in self.resources:
            self.resources[resource_type] = dict()
        self.logger.debug('Registering REST resource %s of type %s at path %s' % (func, resource_type, path))
        self.resources[resource_type][path] = func

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.takes(dict(resource_type=str, path=str))
    @clacks.decorators.returns(object)
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
            msg = 'Resource type %s is not recognized!' % resource_type
            self.logger.error(msg)
            raise KeyError(msg)

        if path not in self.resources[resource_type]:
            msg = 'Resource %s of type %s could not be found!' % (path, resource_type)
            self.logger.error(msg)
            raise NotImplementedError(msg)

        return self.resources[resource_type][path]

    # ------------------------------------------------------------------------------------------------------------------
    def _method(self, method, *args, **kwargs):
        if 'path' not in kwargs:
            raise KeyError('No path provided!')

        path = kwargs.get('path')
        del kwargs['path']

        try:
            resource = self.get_resource(method, path)

        except KeyError:
            return None, clacks.ReturnCodes.SERVER_ERROR

        except NotImplementedError:
            return None, clacks.ReturnCodes.NOT_FOUND

        return resource(*args, **kwargs), clacks.ReturnCodes.OK

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.returns(None)
    @clacks.decorators.returns_status_code
    def POST(self, *args, **kwargs):
        """
        Catch-all POST method, receives POST requests and forwards them to the _method private method. Will return the
        result of whatever method is retrieved by the given resource path.

        :return: Whatever the result of the call is
        :rtype: object
        """
        return self._method('POST', *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.returns(None)
    @clacks.decorators.returns_status_code
    def GET(self, *args, **kwargs):
        """
        Catch-all GET method, receives GET requests and forwards them to the _method private method. Will return the
        result of whatever method is retrieved by the given resource path.

        :return: Whatever the result of the call is
        :rtype: object
        """
        return self._method('GET', *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.returns(None)
    @clacks.decorators.returns_status_code
    def PUT(self, *args, **kwargs):
        """
        Catch-all PUT method, receives PUT requests and forwards them to the _method private method. Will return the
        result of whatever method is retrieved by the given resource path.

        :return: Whatever the result of the call is
        :rtype: object
        """
        return self._method('PUT', *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.returns(None)
    @clacks.decorators.returns_status_code
    def PATCH(self, *args, **kwargs):
        """
        Catch-all PATCH method, receives PATCH requests and forwards them to the _method private method. Will return the
        result of whatever method is retrieved by the given resource path.

        :return: Whatever the result of the call is
        :rtype: object
        """
        return self._method('PATCH', *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.returns(None)
    @clacks.decorators.returns_status_code
    def DELETE(self, *args, **kwargs):
        """
        Catch-all DELETE method, receives DELETE requests and forwards them to the _method private method. Will return the
        result of whatever method is retrieved by the given resource path.

        :return: Whatever the result of the call is
        :rtype: object
        """
        return self._method('DELETE', *args, **kwargs)


clacks.register_server_interface_type('web_core', ClacksCoreWebAPIInterface)
