from wiki2vid.script import ScriptNode
from wiki2vid.wiki import Wiki


class State:
    def __init__(self, wiki_url: str):
        self.wiki = Wiki(wiki_url)
        self.script = ScriptNode("Outline")
        self.brainstorm = ""
