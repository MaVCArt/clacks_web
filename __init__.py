from .core.adapters.browser_adapter import FirefoxHeaderAdapter
from .core.adapters import HeaderKwargAdapter, CORSHeaderAdapter
from .core.html_marshaller import HTMLMarshaller
from .core.http_handler import HTTPHandler
from .core.interfaces import ClacksCoreWebAPIInterface, basic_rest_interface
from clacks_web.core.utils.simple_rest_api import simple_rest_api_from_server, simple_rest_api
from clacks_web.core.decorators.rest_decorators import get, put, post, patch, delete
