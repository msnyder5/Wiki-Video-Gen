from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING, List, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from markdown_it import MarkdownIt
from markdown_it.token import Token

from wiki2vid.ai import AI
from wiki2vid.config import CONFIG
from wiki2vid.scripter.script import Script
from wiki2vid.wiki import Wiki


class Outliner:
    def __init__(self, wiki: Wiki, ai: AI):
        self.wiki = wiki
        self.ai = ai

    @lru_cache
    def _brainstorming(self) -> str:
        messages = [
            SystemMessage(content=CONFIG.prompts.outline.brainstorm),
            HumanMessage(content=self.wiki.content),
        ]
        return self.ai.infer(messages, "brainstorming.md")

    @lru_cache
    def _raw_outline(self) -> str:
        messages = [
            SystemMessage(content=CONFIG.prompts.outline.brainstorm),
            HumanMessage(content=self.wiki.content),
            AIMessage(content=self._brainstorming()),
            SystemMessage(content=CONFIG.prompts.outline.write),
        ]
        return self.ai.infer(messages, "outline.md")

    @lru_cache
    def outline(self) -> Script:
        return Script.from_markdown(self._raw_outline())
