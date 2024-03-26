from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING, List, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from markdown_it import MarkdownIt
from markdown_it.token import Token

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.wiki import Wiki


class Script:
    def __init__(
        self,
        title: str,
        *,
        description: str = "",
        children: Optional[List[Script]] = None,
        script: str = "",
        level: int = 1,
    ):
        self.title = title
        self.description = description
        self.children = children or []
        self.script = script
        self.level = level

    @property
    def outline_spec(self) -> str:
        return f"{'#'*self.level} {self.title}\n\n{self.description}"

    @property
    def partial_script(self) -> str:
        return f"{'#'*self.level} {self.title}\n\n{self.script}"

    @property
    def children_script(self) -> str:
        return "\n\n".join(child.partial_script for child in self.children)

    @property
    def full_script(self) -> str:
        ret = self.partial_script
        if self.children:
            ret += "\n\n"
            ret += self.children_script
        return ret

    @staticmethod
    def from_markdown(markdown: str) -> Script:
        md = MarkdownIt()
        tokens = md.parse(markdown)

        root = Script("Outline")
        stack = [root]

        for i, token in enumerate(tokens):
            if token.type == "heading_open":
                level = int(token.tag[-1])  # e.g., h2 -> 2
                # Close current nodes until reaching the right level in the hierarchy
                while len(stack) > level:
                    stack.pop()

            elif token.type == "inline":
                if tokens[i - 1].type == "heading_open":
                    # This is a title
                    title = token.content
                    new_node = Script(title, level=level)
                    stack[-1].children.append(new_node)
                    stack.append(new_node)
                else:
                    # This is content
                    stack[-1].description += token.content + "\n"
                    stack[-1].description = stack[-1].description

        # Ensure that all nodes content is stripped
        def _strip_content(node: Script):
            node.description = node.description.strip()
            for child in node.children:
                _strip_content(child)

        _strip_content(root)

        return root

    def __str__(self) -> str:
        def _to_markdown(node: Script, level: int) -> str:
            markdown = f"{'#' * level} {node.title}\n\n"
            if node.description:
                markdown += f"{node.description}\n\n"
            for child in node.children:
                markdown += _to_markdown(child, level + 1)
            return markdown

        return "".join(_to_markdown(child, 1) for child in self.children)
