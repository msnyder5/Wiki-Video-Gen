import re
from typing import TYPE_CHECKING

import requests

from wiki2vid.ai import AI
from wiki2vid.prompts import Prompts

if TYPE_CHECKING:
    from wiki2vid import Wiki2Vid


class ScriptBuilder:
    def __init__(self, wiki2vid: Wiki2Vid):
        self.wiki2vid = wiki2vid
        self.base_folder = f"{wiki2vid.base_folder}/script"

    def build_script(self) -> str:
        self.wiki_content = self._wiki_content()
        self.brainstorm = self._brainstorm()
        self.brainstorm_choose = self._brainstorm_choose()
        self.outline = self._outline()
        self.script = self._script()
        return self.script

    def _wiki_content(self) -> str:
        raw_content_url = self.wiki2vid.wiki_url + "?action=raw"
        response = requests.get(raw_content_url)
        return response.text if response.status_code == 200 else ""

    def _brainstorm(self) -> str:
        print("Brainstorming...")
        messages = Prompts.brainstorm.format_messages(wiki_content=self.wiki_content)
        return AI.infer(messages, f"{self.base_folder}/brainstorm.md")

    def _brainstorm_choose(self) -> str:
        messages = Prompts.brainstorm_choose.format_messages(
            wiki_content=self.wiki_content, brainstorm=self.brainstorm
        )
        return AI.infer(messages, f"{self.base_folder}/brainstorm_choose.md")

    def _outline(self) -> str:
        print("Writing outline...")
        messages = Prompts.outline.format_messages(
            wiki_content=self.wiki_content,
            brainstorm=self.brainstorm_choose,
        )
        return AI.infer(messages, f"{self.base_folder}/outline.md")

    def _script(self) -> str:
        print("Writing script...")
        messages = Prompts.write.format_messages(
            wiki_content=self.wiki_content,
            video_outline=self.outline,
        )
        formatter = lambda x: re.sub(
            r"\n\n+", "\n\n", re.sub(r"\*\*[^\*]+\*\*\n|#+ [^\n]+\n", r"", x)
        )
        return AI.infer(messages, f"{self.base_folder}/script.md", formatter=formatter)
