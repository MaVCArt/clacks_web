import clacks
import unittest
import clacks_web


# ----------------------------------------------------------------------------------------------------------------------
class TestFirefoxHandlerAdapter(unittest.TestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test_process_header_data(self):
        adapter = clacks_web.FirefoxHeaderAdapter()
        package = clacks.package.Package(payload=dict())

        adapter.handler_pre_respond(None, None, None, 'unittest', package)

        if not package.header_data:
            self.fail('header data was not injected!')
