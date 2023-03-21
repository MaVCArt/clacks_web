from .adapters.browser_adapter import FirefoxHeaderAdapter
from .adapters.header_kwargs import HeaderKwargAdapter
from .adapters.cors_adapter import CORSHeaderAdapter

from .html_marshaller import HTMLMarshaller
from .http_handler import HTTPHandler

from .simple_web import simple_web_server
from .simple_web import simple_website

from .interfaces.core_interface import ClacksCoreWebAPIInterface

from .rest_decorators import post, get, put, patch, delete
from .simple_rest_api import simple_rest_api_from_server
from .simple_rest_api import simple_rest_api

from . import basic_rest_interface
