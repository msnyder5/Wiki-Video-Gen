from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING, List, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from markdown_it import MarkdownIt
from markdown_it.token import Token

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.scripter.script import Script
from wiki2vid.state import State


class Outliner:
    def __init__(self, state: State):
        self.wiki = state.wiki

    @lru_cache
    def _brainstorming(self) -> str:
        messages = [
            SystemMessage(content=Config.prompts.outline.brainstorm),
            HumanMessage(content=self.wiki.content),
        ]
        return AI.infer(messages, "brainstorming.md")

    @lru_cache
    def _raw_outline(self) -> str:
        messages = [
            SystemMessage(content=Config.prompts.outline.brainstorm),
            HumanMessage(content=self.wiki.content),
            AIMessage(content=self._brainstorming()),
            SystemMessage(content=Config.prompts.outline.write),
        ]
        return AI.infer(messages, "outline.md")

    @lru_cache
    def outline(self) -> Script:
        return Script.from_markdown(self._raw_outline())
