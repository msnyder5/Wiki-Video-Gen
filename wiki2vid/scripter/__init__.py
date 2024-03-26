from wiki2vid.ai import AI
from wiki2vid.scripter.outliner import Outliner, Script
from wiki2vid.scripter.sectioner import Sectioner
from wiki2vid.wiki import Wiki


class Scripter:
    def __init__(self, wiki: Wiki):
        self.wiki = wiki
        self.ai = AI()

    def create_script(self) -> Script:
        outliner = Outliner(self.wiki, self.ai)
        outline = outliner.outline()
        sectioner = Sectioner(outline, self.wiki, self.ai)
        sectioner.write_sections()
        return outline
