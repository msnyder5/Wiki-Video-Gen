from wiki2vid.script.outline import Outline, Script
from wiki2vid.script.section import Section
from wiki2vid.state import State


class ScriptHandler:
    def __init__(self, state: State):
        self.state = state

    def create_script(self) -> Script:
        outline = Outline(self.state)
        self.state.script = outline.empty_script()
        section = Section(self.state)
        section.write_sections()
        return self.state.script
