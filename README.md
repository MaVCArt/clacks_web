```pip install git+https://github.com/MaVCArt/clacks_web.git@main```

# clacks_web

`clacks_web` is a basic extension library for `clacks`, providing common web-based interfaces for things like websites
and REST APIs

This layer is relatively lightweight, as it just provides the extension layer for users to build their own interfaces
with. However, Because it is so simple, most types of web-based interfaces can easily be built with this utility.


## Setting up a REST API with `clacks`

Creating a simple rest API is dead simple. Just the provided utility method from `clacks_web`;

```python
import clacks_web

server = clacks_web.simple_rest_api('MyFirstRESTAPI', 'localhost', 6000)
server.start(blocking=False)
```

Once the server is started, querying this server can be done using the standard `requests` module.

```python
import requests

result = requests.get('http://localhost:6000')
result = result.json()
print(result)
```

A standard GET request on a `clacks_web` server, in default setup, will result in calling the "list_methods" method,
which just returns a list of all the publicly accessible API endpoints and registered Server Commands.

Of course, the example above does not really give you much - just a simple empty REST API with a few example methods.
However, since this framework is built on top of `clacks`, no changes needed to be made to allow our REST API to 
register new methods. All existing practices like Interfaces and Adapters still work.
