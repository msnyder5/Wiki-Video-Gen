from wiki2vid.scripter.outliner import Outliner, Script
from wiki2vid.scripter.sectioner import Sectioner
from wiki2vid.state import State


class Scripter:
    def __init__(self, state: State):
        self.state = state

    def create_script(self) -> Script:
        outliner = Outliner(self.state)
        outline = outliner.outline()
        sectioner = Sectioner(self.state)
        sectioner.write_sections()
        return outline
