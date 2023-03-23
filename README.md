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
