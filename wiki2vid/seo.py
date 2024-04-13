from typing import TYPE_CHECKING

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.prompts import Prompts
from wiki2vid.script import ScriptBuilder
from wiki2vid.segment import Content

if TYPE_CHECKING:
    from wiki2vid import Wiki2Vid


class SEOBuilder:
    def __init__(self, wiki2vid: Wiki2Vid):
        self.base_folder = f"{wiki2vid.base_folder}/seo"
        self.script = wiki2vid.script_builder.script

    def build_seo(self) -> None:
        self.video_title = self._video_title()
        self.video_description = self._video_description()

    def _video_title(self) -> str:
        messages = Prompts.video_title.format_messages(script=self.script)
        formatter = lambda x: x.strip("\" '")
        return AI.infer(
            messages, f"{self.base_folder}/video_title.md", formatter=formatter
        )

    def _video_description(self) -> str:
        messages = Prompts.video_description.format_messages(script=self.script)
        return AI.infer(messages, f"{self.base_folder}/video_description.md")
