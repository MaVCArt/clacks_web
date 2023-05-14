# ----------------------------------------------------------------------------------------------------------------------
def resource(path, method, expose_as_method=False):
    # type: (str, str, bool) -> callable
    """
    Generic resource, requires that you declare an all-upper-case method type.

    :param path: the URL to the resource, relative to the master page. Starts with '/'
    :type path: str

    :param method: The method to expose this resource under. Examples are POST, GET, PUT, DELETE, PATCH
    :type method: str

    :param expose_as_method: If True, will not register this method as a server command.
    :type expose_as_method: bool

    :return: the decorated method
    :rtype: callable
    """
    def wrapper(fn):
        fn.resource_type = method.upper()
        fn.path = path
        # -- if the user doesn't want the decorated method to be registered as a server command, the "expose as method"
        # -- argument can be set to False, which will mark the method as private.
        if not expose_as_method:
            fn.hidden = True
        return fn
    return wrapper


# ----------------------------------------------------------------------------------------------------------------------
def post(path, expose_as_method=False):
    # type: (str, bool) -> callable
    """
    Generic resource, requires that you declare an all-upper-case method type.

    :param path: the URL to the resource, relative to the master page. Starts with '/'
    :type path: str

    :param expose_as_method: If True, will not register this method as a server command.
    :type expose_as_method: bool

    :return: the decorated method
    :rtype: callable
    """
    def wrapper(fn):
        fn.resource_type = 'POST'
        fn.path = path
        # -- if the user doesn't want the decorated method to be registered as a server command, the "expose as method"
        # -- argument can be set to False, which will mark the method as private.
        if not expose_as_method:
            fn.hidden = True
        return fn
    return wrapper


# ----------------------------------------------------------------------------------------------------------------------
def get(path, expose_as_method=False):
    # type: (str, bool) -> callable
    """
    Generic resource, requires that you declare an all-upper-case method type.

    :param path: the URL to the resource, relative to the master page. Starts with '/'
    :type path: str

    :param expose_as_method: If True, will not register this method as a server command.
    :type expose_as_method: bool

    :return: the decorated method
    :rtype: callable
    """
    def wrapper(fn):
        fn.resource_type = 'GET'
        fn.path = path
        # -- if the user doesn't want the decorated method to be registered as a server command, the "expose as method"
        # -- argument can be set to False, which will mark the method as private.
        if not expose_as_method:
            fn.hidden = True
        return fn
    return wrapper


# ----------------------------------------------------------------------------------------------------------------------
def put(path, expose_as_method=False):
    # type: (str, bool) -> callable
    """
    Generic resource, requires that you declare an all-upper-case method type.

    :param path: the URL to the resource, relative to the master page. Starts with '/'
    :type path: str

    :param expose_as_method: If True, will not register this method as a server command.
    :type expose_as_method: bool

    :return: the decorated method
    :rtype: callable
    """
    def wrapper(fn):
        fn.resource_type = 'PUT'
        fn.path = path
        # -- if the user doesn't want the decorated method to be registered as a server command, the "expose as method"
        # -- argument can be set to False, which will mark the method as private.
        if not expose_as_method:
            fn.hidden = True
        return fn
    return wrapper


# ----------------------------------------------------------------------------------------------------------------------
def patch(path, expose_as_method=False):
    # type: (str, bool) -> callable
    """
    Generic resource, requires that you declare an all-upper-case method type.

    :param path: the URL to the resource, relative to the master page. Starts with '/'
    :type path: str

    :param expose_as_method: If True, will not register this method as a server command.
    :type expose_as_method: bool

    :return: the decorated method
    :rtype: callable
    """
    def wrapper(fn):
        fn.resource_type = 'PATCH'
        fn.path = path
        # -- if the user doesn't want the decorated method to be registered as a server command, the "expose as method"
        # -- argument can be set to False, which will mark the method as private.
        if not expose_as_method:
            fn.hidden = True
        return fn
    return wrapper


# ----------------------------------------------------------------------------------------------------------------------
def delete(path, expose_as_method=False):
    # type: (str, bool) -> callable
    """
    Generic resource, requires that you declare an all-upper-case method type.

    :param path: the URL to the resource, relative to the master page. Starts with '/'
    :type path: str

    :param expose_as_method: If True, will not register this method as a server command.
    :type expose_as_method: bool

    :return: the decorated method
    :rtype: callable
    """
    def wrapper(fn):
        fn.resource_type = 'DELETE'
        fn.path = path
        # -- if the user doesn't want the decorated method to be registered as a server command, the "expose as method"
        # -- argument can be set to False, which will mark the method as private.
        if not expose_as_method:
            fn.hidden = True
        return fn
    return wrapper
