import os
import clacks
import functools


# ----------------------------------------------------------------------------------------------------------------------
class ClacksBasicWebsiteInterface(clacks.ServerInterface):

    _REQUIRED_INTERFACES = ['website_utils']

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        super(ClacksBasicWebsiteInterface, self).__init__()
        self.tokens = dict()
        self.resource_filters = dict()
        self.environment = None

    # ------------------------------------------------------------------------------------------------------------------
    def _initialize(self, parent):  # type: () -> bool
        success = super(ClacksBasicWebsiteInterface, self)._initialize(parent)
        if not success:
            return False

        self.register_token('server', self.server)
        self.register_token('str', str)

        return True

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.private
    def register_resource_filter(self, pattern, _filter):
        if not callable(_filter):
            raise ValueError(_filter)
        self.resource_filters[pattern] = _filter

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.private
    def register_root_directory(self, directory):
        try:
            from jinja2 import Environment, FileSystemLoader
            self.environment = Environment(loader=FileSystemLoader(searchpath=directory))
        except ImportError:
            self.environment = NotImplementedError

        for root, dirs, files in os.walk(directory):
            for f in files:
                path = os.path.join(root, f)
                resource_path = path.replace(directory, '').replace('\\', '/')

                self.server.register_resource(
                    'GET',
                    resource_path,
                    functools.partial(self.get_file_resource, path)
                )

        if os.path.exists(os.path.join(directory, 'index.html')):
            self.server.register_resource(
                'GET',
                '/',
                functools.partial(self.get_file_resource, os.path.join(directory, 'index.html'))
            )

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.hidden
    def get_file_resource(self, path, *args, **kwargs):
        if not os.path.exists(path):
            return 'Resource not found!'

        with open(path, 'rb') as fp:
            try:
                contents = fp.read()
            except:
                raise Exception('Could not read file resource {}'.format(path))

        try:
            contents = contents.decode('utf-8')
        except:
            return contents

        for pattern in self.resource_filters:
            if pattern not in path:
                continue
            contents = self.resource_filters[pattern](contents)

        result = self.render(contents)

        if 'highlight' in kwargs:
            result = self.server.highlight_text(result, kwargs['highlight'])

        return result

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.hidden
    def render(self, contents):
        if self.environment is NotImplementedError:
            return 'jinja2 could not be imported - cannot render contents!\n{}'.format(contents)
        return self.environment.from_string(contents).render(**self.tokens)

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.takes(arg_types=dict(token=str, value=object))
    @clacks.decorators.returns(None)
    @clacks.decorators.process_arguments([clacks.arg_processors.auto_strip_args])
    def register_token(self, token, value):
        """
        Register a token to use when rendering website contents with jinja2. This token can be any object, and will be
        made available for jinja templates to use. This is callable as a server command, because it could allow a client
        to enhance the website template with some basic JSON-compatible objects.

        :param token: Token name to register
        :type token: str

        :param value: Token to register
        :type value: object

        :return: None
        :rtype: None
        """
        self.tokens[token] = value


clacks.register_server_interface_type('website_basic', ClacksBasicWebsiteInterface)
