from __future__ import annotations

from enum import Enum
from typing import List, Optional

from markdown_it import MarkdownIt

from wiki2vid.config import Config


class MDType(Enum):
    OUTLINE = 1
    SECTION = 2


class ScriptNode:
    def __init__(
        self,
        title: str,
        description: str = "",
        content: str = "",
        children: Optional[List[ScriptNode]] = None,
        level: int = 0,
        parent_filepath: str = Config.folder,
    ):
        self.title: str = title
        self.description: str = description
        self.content: str = content
        self.children: List[ScriptNode] = children or []
        self.level = level
        self.filepath: str = f"{parent_filepath}/{title}.md"

    def update_from_outline_markdown(self, outline: str) -> None:
        self._update_from_markdown(outline, type=MDType.OUTLINE)

    def update_from_script_markdown(self, script: str) -> None:
        self._update_from_markdown(script, type=MDType.SECTION)

    def _update_from_markdown(self, markdown: str, type: MDType) -> None:
        md = MarkdownIt()
        tokens = md.parse(markdown)
        stack: List[ScriptNode] = [self]
        for i, token in enumerate(tokens):
            if token.type == "heading_open":
                level = int(token.tag[-1])
                while len(stack) > (level - self.level):
                    stack.pop()
            elif token.type == "inline":
                if tokens[i - 1].type == "heading_open":
                    title = token.content
                    node = self._find_or_create_child(title)
                    stack[-1].children.append(node)
                    stack.append(node)
                else:
                    if type == MDType.OUTLINE:
                        stack[-1].description += token.content + "\n"
                        stack[-1].description = stack[-1].description
                    elif type == MDType.SECTION:
                        stack[-1].content += token.content + "\n"
                        stack[-1].content = stack[-1].content

        self._strip_content()

    def _find_or_create_child(self, title: str) -> ScriptNode:
        for child in self.children:
            if child.title == title:
                return child
        new_child = ScriptNode(
            title, parent_filepath=self.filepath, level=self.level + 1
        )
        self.children.append(new_child)
        return new_child

    def _strip_content(self):
        self.description = self.description.strip()
        for child in self.children:
            child._strip_content()

    @property
    def outline_info(self) -> str:
        return f"{'#'*self.level} {self.title}\n\n{self.description}"

    @property
    def self_script(self) -> str:
        return f"{'#'*self.level} {self.title}\n\n{self.content}"

    @property
    def children_script(self) -> str:
        return "\n\n".join(child.self_script for child in self.children)

    @property
    def script(self) -> str:
        ret = self.self_script
        if self.children:
            ret += "\n\n"
            ret += self.children_script
        return ret

    def __str__(self) -> str:
        return self._to_markdown()

    def _to_markdown(self) -> str:
        markdown = f"{'#' * self.level} {self.title}\n\n"
        if self.description:
            markdown += f"{self.description}\n\n"
        for child in self.children:
            markdown += child._to_markdown()
        return markdown


class Script:
    def __init__(self, root: ScriptNode):
        self.root = root

    def __str__(self) -> str:
        return "".join(str(child) for child in self.root.children)
