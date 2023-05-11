import re
import clacks


# ----------------------------------------------------------------------------------------------------------------------
class ClacksWebsiteUtilsInterface(clacks.ServerInterface):

    # ------------------------------------------------------------------------------------------------------------------
    @clacks.decorators.hidden
    def highlight_text(self, body, pattern):
        from bs4 import BeautifulSoup
        html = BeautifulSoup(body, 'html.parser')
        for tag in html.find_all(text=re.compile(pattern)):
            if pattern not in tag:
                continue
            new_tag = BeautifulSoup('<span class="highlighted">{}</span>'.format(pattern), 'html.parser')
            tag.replace_with(new_tag)
        return str(html)


clacks.register_server_interface_type('website_utils', ClacksWebsiteUtilsInterface)
