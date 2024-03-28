from typing import Dict, List, Union

from langchain_core.messages import HumanMessage

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.segment import Content, SegmentNode


class ScriptBuilder:
    def __init__(self, content: Content):
        self.wiki = content.wiki
        self.brainstorm = ""
        self.outline = ""

    def create_script(self) -> None:
        self._brainstorm()
        self._write_outline()
        self._write_script()

    def _brainstorm(self) -> str:
        messages = Config.prompts.brainstorm.format_messages(
            wiki_content=self.wiki.content
        )
        brainstorm = AI.infer(messages, f"{Config.folder}/brainstorm.md")
        messages = Config.prompts.brainstorm_choose.format_messages(
            wiki_content=self.wiki.content, brainstorm=brainstorm
        )
        self.brainstorm = AI.infer(messages, f"{Config.folder}/brainstorm_choose.md")
        return self.brainstorm

    def _write_outline(self) -> str:
        messages = Config.prompts.outline.format_messages(
            wiki_content=self.wiki.content,
            brainstorm=self.brainstorm,
        )
        self.outline = AI.infer(messages, f"{Config.folder}/outline.md")
        return self.outline

    def _write_script(self) -> str:
        messages = Config.prompts.whole_write.format_messages(
            wiki_content=self.wiki.content,
            video_outline=self.outline,
        )
        self.content = AI.infer(messages, f"{Config.folder}/script.md")
        return self.content
