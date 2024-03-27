from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from markdown_it import MarkdownIt

from wiki2vid.config import Config
from wiki2vid.wiki import Wiki


class MDType(Enum):
    OUTLINE = 1
    SECTION = 2


@dataclass
class SegmentScript:
    title: str
    description: str
    notes: str
    content: str
    segment: SegmentNode

    def __str__(self) -> str:
        return self.script

    @property
    def self_outline(self) -> str:
        ret = f"{'#'*self.segment.level} {self.title}"
        if self.description:
            ret += f"\n\n{self.description}"
        return ret

    @property
    def children_outline(self) -> str:
        return "\n\n".join(child.script.outline for child in self.segment.children)

    @property
    def outline(self) -> str:
        return (
            f"{self.self_outline}\n\n{self.children_outline}"
            if self.segment.children
            else self.self_outline
        )

    @property
    def self_script(self) -> str:
        ret = f"{'#'*self.segment.level} {self.title}"
        if self.content:
            ret += f"\n\n{self.content}"
        return ret

    @property
    def children_script(self) -> str:
        return "\n\n".join(child.script.self_script for child in self.segment.children)

    @property
    def script(self) -> str:
        return (
            f"{self.self_script}\n\n{self.children_script}"
            if self.segment.children
            else self.self_script
        )

    def update_from_outline_markdown(self, outline: str) -> None:
        self._update_from_markdown(outline, type=MDType.OUTLINE)

    def update_from_script_markdown(self, script: str) -> None:
        self._update_from_markdown(script, type=MDType.SECTION)

    def _update_from_markdown(self, markdown: str, type: MDType) -> None:
        if type == MDType.OUTLINE:
            self.description = ""
        elif type == MDType.SECTION:
            self.content = ""
        md = MarkdownIt()
        tokens = md.parse(markdown)
        stack: List[SegmentScript] = [self]
        for i, token in enumerate(tokens):
            pass
            if token.type == "heading_open":
                level = int(token.tag[-1]) - 1
                while len(stack) > (level - self.segment.level):
                    popped = stack.pop()
                    popped._strip()
            elif token.type == "inline":
                if tokens[i - 1].type == "heading_open":
                    title = token.content
                    node = stack[-1]._find_or_create_child(title)
                    if type == MDType.OUTLINE:
                        node.description = ""
                    elif type == MDType.SECTION:
                        node.content = ""
                    stack.append(node)
                elif token.content.strip():
                    if type == MDType.OUTLINE:
                        stack[-1].description += token.content + "\n\n"
                    elif type == MDType.SECTION:
                        stack[-1].content += token.content + "\n\n"

        self._strip()

    def _find_or_create_child(self, title: str) -> SegmentScript:
        for child in self.segment.children:
            if child.script.title == title:
                return child.script
        new_child = SegmentNode(
            title,
            parent_folder=self.segment.folder,
            level=self.segment.level + 1,
        )
        self.segment.children.append(new_child)
        return new_child.script

    def _strip(self):
        self.description = self.description.strip()
        self.content = self.content.strip()
        for child in self.segment.children:
            child.script._strip()


class SegmentNode:
    def __init__(
        self,
        segment_name: str,
        description: str = "",
        notes: str = "",
        content: str = "",
        search_terms: Optional[List[str]] = None,
        children: Optional[List[SegmentNode]] = None,
        level: int = 0,
        parent_folder: str = Config.folder,
    ):
        self.script = SegmentScript(segment_name, description, notes, content, self)
        self.search_terms: List[str] = search_terms or []
        self.children: List[SegmentNode] = children or []
        self.level = level
        self.folder: str = f"{parent_folder}/{self.script.title}"

    @property
    def nodes(self) -> List[SegmentNode]:
        ret: List[SegmentNode] = [self]
        for child in self.children:
            ret += child.nodes
        return ret

    def __str__(self) -> str:
        return self.script.script


class Content:
    def __init__(self, wiki_url: str, root: Optional[SegmentNode] = None):
        self.wiki = Wiki(wiki_url)
        self.root = root or SegmentNode("Sections")
        self.title = ""
        self.description = ""
        self.brainstorm = ""

    @property
    def clean_nodes(self) -> List[SegmentNode]:
        return self.root.nodes[1:]

    @property
    def script(self) -> str:
        return self.root.script.script

    @property
    def outline(self) -> str:
        return self.root.script.outline

    def __str__(self) -> str:
        return self.root.script.script
