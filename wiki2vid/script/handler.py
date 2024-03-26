from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.script.script import Script
from wiki2vid.state import State


class ScriptHandler:
    def __init__(self, state: State):
        self.state = state

    def create_script(self) -> Script:
        self._brainstorm()
        self._write_outline()
        self._write_sections()
        return self.state.script

    def _brainstorm(self) -> None:
        messages = [
            SystemMessage(content=Config.prompts.outline.brainstorm),
            HumanMessage(content=self.state.wiki.content),
        ]
        self.state.brainstorm = AI.infer(messages, "brainstorming.md")

    def _write_outline(self) -> None:
        messages = [
            SystemMessage(content=Config.prompts.outline.brainstorm),
            HumanMessage(content=self.state.wiki.content),
            AIMessage(content=self.state.brainstorm),
            SystemMessage(content=Config.prompts.outline.write),
        ]
        response = AI.infer(messages, "outline.md")
        self.state.script = Script.from_markdown(response)

    def _write_sections(self) -> None:
        def _write_section(section: Script) -> None:
            if section.children:
                messages = [
                    SystemMessage(content=Config.prompts.section.write),
                    HumanMessage(content=self.state.wiki.content),
                    HumanMessage(content=section.outline_spec),
                ]
            else:
                for child in section.children:
                    _write_section(child)
                children_script = section.children_script
                messages = [
                    SystemMessage(content=Config.prompts.section.write_with_children),
                    HumanMessage(content=self.state.wiki.content),
                    HumanMessage(content=f"**CHILDREN SCRIPTS**\n\n{children_script}"),
                    HumanMessage(content=section.outline_spec),
                ]
            section.script = AI.infer(messages, section.filepath)

        for section in self.state.script.children:
            _write_section(section)
