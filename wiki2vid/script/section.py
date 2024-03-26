from langchain_core.messages import HumanMessage, SystemMessage

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.script.outline import Script
from wiki2vid.state import State


class Section:
    def __init__(self, state: State):
        self.state = state

    def write_section(self, section: Script, level: int = 1) -> None:
        if section.children:
            for child in section.children:
                self.write_section(child, level + 1)
            children_script = section.children_script
            messages = [
                SystemMessage(content=Config.prompts.section.write_with_children),
                HumanMessage(content=self.state.wiki.content),
                HumanMessage(content=f"**CHILDREN SCRIPTS**\n\n{children_script}"),
                HumanMessage(content=section.outline_spec),
            ]
        else:
            messages = [
                SystemMessage(content=Config.prompts.section.write),
                HumanMessage(content=self.state.wiki.content),
                HumanMessage(content=section.outline_spec),
            ]
        section.script = AI.infer(messages, section.filepath)

    def write_sections(self) -> None:
        for section in self.state.script.children:
            self.write_section(section)
