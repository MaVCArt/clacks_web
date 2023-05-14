import collections

from clacks.core.handler import BaseRequestHandler
from clacks.core.handler import register_handler_type
from clacks.core.package import Question, Response, Package


# ----------------------------------------------------------------------------------------------------------------------
class HTTPHandler(BaseRequestHandler):

    # ------------------------------------------------------------------------------------------------------------------
    def _header_to_dict(self, header):
        # type: (str) -> tuple
        data = str(header.decode(self.FORMAT))

        flags = dict()
        lines = list()

        method = data.splitlines()[0]

        for line in data.splitlines()[1:]:
            if not line.strip():
                continue
            if ':' not in line:
                continue
            lines.append(line.strip())

        for line in lines:
            key, _, value = line.partition(': ')
            flags[key] = value

        return method, flags

    # ------------------------------------------------------------------------------------------------------------------
    def decode_question_header(self, transaction_id, header):
        # type: (str, bytes) -> dict
        method, result = self._header_to_dict(header)

        # -- third part is the HTTP version
        method, path, _ = method.split(' ')
        result['command'] = method

        if 'Access-Control-Request-Method' in result:
            result['command'] = result['Access-Control-Request-Method']

        # -- inject path argument
        result['path'] = path.rpartition('?')[0] if '?' in path else path

        # -- get keyword args from the passed parameters
        kwargs = dict()

        if '?' in path:
            kwarg_string = path.rpartition('?')[2]
            pairs = kwarg_string.split('&')
            for pair in pairs:
                key, _, value = pair.partition('=')
                kwargs[key] = value

        result['kwargs'] = kwargs
        result['Accept-Encoding'] = result.get('Accept-Encoding', 'text/json')

        return result

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def dict_to_header(cls, data):
        result = ''
        for key, value in data.items():
            result += '%s: %s\n' % (key, str(value).strip('\n\r'))
        return result.strip('\n')

    # ------------------------------------------------------------------------------------------------------------------
    def _get_header_data(self, transaction_id, payload, header_data):
        # type: (str, Package, collections.OrderedDict) -> collections.OrderedDict
        if payload.keep_alive:
            header_data['Connection'] = 'keep-alive'
        header_data['Accept-Encoding'] = payload.accept_encoding
        header_data['Content-Length'] = self.get_content_length(transaction_id, payload)
        return header_data

    # ------------------------------------------------------------------------------------------------------------------
    def encode_question_header(self, transaction_id, payload, expected_content_length):
        # type: (str, Question, int) -> bytes
        data = '%s %s HTTP/1.1\n' % (payload.command, payload.kwargs.get('path', '/'))
        data += self.dict_to_header(self.get_outgoing_header_data(transaction_id, payload, expected_content_length))
        return bytes(data, self.FORMAT)

    # ------------------------------------------------------------------------------------------------------------------
    def decode_response_header(self, transaction_id, header):
        # type: (str, bytes) -> dict
        method, result = self._header_to_dict(header)
        protocol, _, parts = method.partition(' ')
        ret_code, _, reason = parts.partition(' ')
        result['code'] = int(ret_code)
        result['Accept-Encoding'] = result.get('Accept-Encoding', 'text/json')
        return result

    # ------------------------------------------------------------------------------------------------------------------
    def encode_response_header(self, transaction_id, payload, expected_content_length):
        # type: (str, Response, int) -> bytes
        # -- if this outgoing, it will not
        error = ''

        if payload.traceback:
            error = payload.traceback.splitlines()[-2]

        if payload.errors:
            error = payload.errors[-1]

        data = 'HTTP/1.1 %s %s\n' % (payload.code, 'OK' if not error else error)
        data += self.dict_to_header(self.get_outgoing_header_data(transaction_id, payload, expected_content_length))
        return bytes(data, self.FORMAT)


register_handler_type('http', HTTPHandler)
