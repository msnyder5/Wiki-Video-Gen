from typing import List

from langchain_core.messages import HumanMessage, SystemMessage

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.scripter.outliner import Script
from wiki2vid.wiki import Wiki


class Sectioner:
    def __init__(self, outline: Script, wiki: Wiki, ai: AI):
        self.outline = outline
        self.wiki = wiki
        self.ai = ai

    def write_section(self, section: Script, level: int = 1) -> None:
        if section.children:
            for child in section.children:
                self.write_section(child, level + 1)
            children_script = section.children_script
            messages = [
                SystemMessage(content=Config.prompts.section.write_with_children),
                HumanMessage(content=self.wiki.content),
                HumanMessage(content=f"**CHILDREN SCRIPTS**\n\n{children_script}"),
                HumanMessage(content=section.outline_spec),
            ]
        else:
            messages = [
                SystemMessage(content=Config.prompts.section.write),
                HumanMessage(content=self.wiki.content),
                HumanMessage(content=section.outline_spec),
            ]
        section.script = self.ai.infer(messages, f"{section.title}.md")

    def write_sections(self) -> None:
        for section in self.outline.children:
            self.write_section(section)
