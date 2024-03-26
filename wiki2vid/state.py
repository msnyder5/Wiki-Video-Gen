from wiki2vid.script import Script
from wiki2vid.wiki import Wiki


class State:
    def __init__(self, wiki_url: str):
        self.wiki = Wiki(wiki_url)
        self.script = Script("Outline")
        self.brainstorm = ""
