import os
import json
import urllib

from clacks.core.package import Package
from clacks.core.marshaller import BasePackageMarshaller
from clacks.core.marshaller import register_marshaller_type


# ----------------------------------------------------------------------------------------------------------------------
class HTMLMarshaller(BasePackageMarshaller):

    DEFAULT_RAW_RESPONSE = False

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_transaction_cache(cls, transaction_id):
        path = os.path.join(os.getenv('TEMP'), 'ClacksTransactionCache', transaction_id)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def clear_transaction_cache(cls, transaction_id):
        path = cls.get_transaction_cache(transaction_id)
        if not os.path.isdir(path):
            return True

        # -- clear the entire cache
        for root, dirs, files in os.walk(path):
            for f in files:
                p = os.path.join(root, f)
                os.unlink(p)

            for d in dirs:
                p = os.path.join(root, d)
                os.rmdir(p)

        # -- then delete it
        os.rmdir(path)

        return True

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def download_file(cls, transaction_id, filename, body):
        # -- ensure the transaction cache exists
        path = cls.get_transaction_cache(transaction_id)

        file_path = os.path.join(path, filename)
        with open(file_path, 'w+b') as fp:
            fp.write(body)

        return file_path

    # ------------------------------------------------------------------------------------------------------------------
    def _encode_package(self, transaction_id, package):
        # type: (str, Package) -> bytes
        if self.raw_response_requested(transaction_id):
            payload = package.payload
            result = 'value=%s' % json.dumps(payload)

        elif 'response' in package.payload:
            result = str(package.payload.get('response'))

        else:
            result = str(package.payload)

        return bytes(result, self.encoding)

    # ------------------------------------------------------------------------------------------------------------------
    def _decode_package(self, transaction_id, header_data, payload):
        # type: (str, dict, bytes) -> dict
        data = payload

        result = dict()

        if 'multipart/form-data' in header_data.get('Content-Type', ''):
            boundary = header_data.get('Content-Type')
            boundary = boundary.rpartition('; ')[2]
            boundary = boundary[len('boundary='):]

            parts, data = self.handle_multipart(transaction_id, data, boundary)

            # -- if we're dealing with forms, the 'command' field is the command argument.
            if 'command' in parts:
                result['command'] = parts['command']
                del parts['command']

            # -- if we're dealing with forms, we consider form fields to be keyword arguments
            result['kwargs'] = parts

        for line in data.splitlines():
            line = urllib.unquote(line)

            if '&' in line:
                for part in line.split('&'):
                    key, _, value = part.partition('=')

                    # -- if we add more than one value to the same argument, that is the HTML protocol for a list.
                    if key in result:
                        result[key] = [result[key]]
                        result[key].append(value)
                        result[key] = list(set(result[key]))

                    else:
                        result[key] = value

            else:
                key, _, value = line.partition('=')
                result[key] = value

        if len(result.keys()) == 1:
            if result.keys()[0] == 'value':
                result = json.loads(result[result.keys()[0]])

        return result

    # ------------------------------------------------------------------------------------------------------------------
    def handle_multipart(self, transaction_id, data, boundary):
        left, _, middle = data.partition('--%s' % boundary)
        middle, _, right = data.partition('--%s--' % boundary)

        parts = middle.split('--%s' % boundary)
        parts = list(part for part in parts if part)

        result = dict()
        for part in parts:
            header, _, body = part.partition('\n\r')
            body = body.lstrip('\n\r').rstrip('\n\r')
            attr_blocks = header.partition('; ')[2].split('; ')

            name = None

            # -- ensure our attribute block exists in the result dict first.
            for attr_block in attr_blocks:
                key, value = attr_block.split('=')

                # -- sanitize our data
                key = key.strip('\r').replace('"', '')
                value = value.strip('\r').replace('"', '')

                if key == 'name':
                    result[value] = dict()
                    name = value

            for attr_block in attr_blocks:
                key, value = attr_block.split('=')

                # -- sanitize our data
                key = key.strip('\r').replace('"', '')
                value = value.strip('\r').replace('"', '')

                if key == 'name':
                    continue

                result[name][key] = value

            if 'filename' in result[name]:
                file_path = self.download_file(transaction_id, result[name]['filename'], body=body)
                result[name] = file_path

            else:
                result[name] = body

        return result, left + right


register_marshaller_type('html', HTMLMarshaller)
