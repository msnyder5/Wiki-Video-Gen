from functools import cached_property

import pypandoc
import requests


class Wiki:
    def __init__(self, url: str):
        self.url = url

    @cached_property
    def content(self) -> str:
        raw_url = self.url + "?action=raw"
        response = requests.get(raw_url)
        if response.status_code == 200:
            return response.text
        else:
            return ""

    @cached_property
    def pretty_content(self) -> str:
        return pypandoc.convert_text(self.content, "md", format="mediawiki")
