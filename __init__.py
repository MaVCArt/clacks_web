from .core.adapters.browser_adapter import FirefoxHeaderAdapter
from .core.adapters import HeaderKwargAdapter, CORSHeaderAdapter
from .core.html_marshaller import HTMLMarshaller
from .core.http_handler import HTTPHandler
from .core.simple_web import simple_web_server
from .core.simple_web import simple_website
from .core.interfaces import ClacksCoreWebAPIInterface
from .core.simple_rest_api import simple_rest_api_from_server, simple_rest_api
from .core.rest_decorators import get, put, post, patch, delete
from .core import basic_rest_interface
