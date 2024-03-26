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
        self.title: str = title.replace(":", "").replace('"', "").replace("'", "")
        self.description: str = description
        self.content: str = content
        self.children: List[ScriptNode] = children or []
        self.level = level
        self.filepath: str = f"{parent_filepath}/{self.title}"
        self.filename: str = f"{self.filepath}.md"

    def update_from_outline_markdown(self, outline: str) -> None:
        self._update_from_markdown(outline, type=MDType.OUTLINE)

    def update_from_script_markdown(self, script: str) -> None:
        self._update_from_markdown(script, type=MDType.SECTION)

    def _update_from_markdown(self, markdown: str, type: MDType) -> None:
        md = MarkdownIt()
        tokens = md.parse(markdown)
        stack: List[ScriptNode] = [self]
        for i, token in enumerate(tokens):
            pass
            if token.type == "heading_open":
                level = int(token.tag[-1]) - 1
                while len(stack) > (level - self.level):
                    stack.pop()
            elif token.type == "inline":
                if tokens[i - 1].type == "heading_open":
                    title = token.content
                    node = stack[-1]._find_or_create_child(title)
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
            title,
            parent_filepath=self.filepath,
            level=self.level + 1,
        )
        self.children.append(new_child)
        return new_child

    def _strip_content(self):
        self.description = self.description.strip()
        for child in self.children:
            child._strip_content()

    @property
    def self_outline(self) -> str:
        ret = f"{'#'*self.level} {self.title}" if self.level else self.title
        if self.description:
            ret += f"\n\n{self.description}"
        return ret

    @property
    def children_outline(self) -> str:
        return "\n\n".join(child.outline for child in self.children)

    @property
    def outline(self) -> str:
        return (
            f"{self.self_outline}\n\n{self.children_outline}"
            if self.children
            else self.self_outline
        )

    @property
    def self_script(self) -> str:
        return f"{'#'*self.level} {self.title}\n\n{self.content}"

    @property
    def children_script(self) -> str:
        return "\n\n".join(child.self_script for child in self.children)

    @property
    def script(self) -> str:
        return "\n\n".join(
            (self.self_script, *(child.script for child in self.children))
        )

    def __str__(self) -> str:
        return self.script


class Script:
    def __init__(self, root: Optional[ScriptNode] = None):
        self.root = root or ScriptNode("Sections")

    @property
    def outline(self) -> str:
        return self.root.outline

    @property
    def script(self) -> str:
        return self.root.script

    def __str__(self) -> str:
        return "".join(str(child) for child in self.root.children)
