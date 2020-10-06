import re
from config.settings import TRACKED_BRANDS_LIST


class Tweet:

    def __init__(self, data):
        self.data = data

    def user_link(self):
        """
        Make links to user's profile page on twitter
        """
        return "http://twitter.com/{}".format(self.data["username"])

    def filtered_text(self):
        return self.filter_brands(self.filter_urls(self.data["text"]))

    def filter_brands(self, text):
        """
        Highlight brands within the text
        """
        for brand in TRACKED_BRANDS_LIST:
            if brand in text:
                text = text.replace(brand, "<mark>{}</mark>".format(brand))
            else:
                continue
        return text

    def filter_urls(self, text):
        """
        Replaces any url within the text with the html <a> tag to make it clickable on the page
        """
        return re.sub("(https?:\/\/\w+(\.\w+)+(\/[\w\+\-\,\%]+)*(\?[\w\[\]]+(=\w*)?(&\w+(=\w*)?)*)?(#\w+)?)",
                      r'<a href="\1" target="_blank">\1</a>',
                      text)
