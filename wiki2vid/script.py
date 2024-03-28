from typing import Dict, List, Union

from langchain_core.messages import HumanMessage

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.segment import Content, SegmentNode


class ScriptBuilder:
    def __init__(self, content: Content):
        self.content = content

    def create_script(self) -> None:
        self._brainstorm()
        self._write_outline()
        self._take_notes()
        self._write_sections()
        self._revise_sections(1)
        # self.revise_sections(2)
        self.smooth_transitions()

    def _brainstorm(self) -> str:
        messages = Config.prompts.brainstorm.format_messages(
            wiki_content=self.content.wiki.content
        )
        brainstorm = AI.infer(messages, f"{Config.folder}/brainstorm.md")
        messages = Config.prompts.brainstorm_choose.format_messages(
            wiki_content=self.content.wiki.content, brainstorm=brainstorm
        )
        self.content.brainstorm = AI.infer(
            messages, f"{Config.folder}/brainstorm_choose.md"
        )
        return self.content.brainstorm

    def _write_outline(self) -> str:
        messages = Config.prompts.outline.format_messages(
            wiki_content=self.content.wiki.content,
            brainstorm=self.content.brainstorm,
        )
        response = AI.infer(messages, f"{Config.folder}/outline.md")
        self.content.root.script.update_from_outline_markdown(response)
        return response

    def _take_notes(self) -> Dict[str, Union[str, Dict]]:
        def _take_notes(section: SegmentNode) -> Union[str, Dict]:
            if section.children:
                return {
                    child.script.title: _take_notes(child) for child in section.children
                }
            messages = Config.prompts.notes.format_messages(
                wiki_content=self.content.wiki.content,
                section_outline=section.script.self_outline,
            )
            section.script.notes = AI.infer(messages, f"{section.folder}/notes.md")
            return section.script.notes

        return {
            section.script.title: _take_notes(section)
            for section in self.content.root.children
        }

    def _write_sections(self) -> Dict[str, Union[str, Dict]]:
        def _write_section(section: SegmentNode) -> Union[str, Dict]:
            if section.children:
                return {
                    child.script.title: _write_section(child)
                    for child in section.children
                }
            else:
                messages = Config.prompts.write.format_messages(
                    wiki_notes=section.script.notes,
                    current_script=self.content.script,
                    section_outline=section.script.self_outline,
                )
                section.script.content = AI.infer(
                    messages, f"{section.folder}/draft.md"
                )
                return section.script.content

        return {
            section.script.title: _write_section(section)
            for section in self.content.root.children
        }

    def _revise_sections(self, rev: int = 1) -> Dict[str, Union[str, Dict]]:
        def _section_feedbacks(section: SegmentNode) -> List[HumanMessage]:
            messages = Config.prompts.feedback.format_messages(
                script=self.content.script,
                section_outline=section.script.self_outline,
                section_content=section.script.content,
            )
            feedbacks = [
                AI.infer(messages, f"{section.folder}/feedback_{rev}_{i+1}.md")
                for i in range(Config.num_feedbacks)
            ]
            return [HumanMessage(content=feedback) for feedback in feedbacks]

        def _revise_section(section: SegmentNode) -> Union[str, Dict]:
            if section.children:
                return {
                    child.script.title: _revise_section(child)
                    for child in section.children
                }
            messages = Config.prompts.revise.format_messages(
                script=self.content.script,
                section_outline=section.script.self_outline,
                section_content=section.script.content,
            ) + _section_feedbacks(section)
            response = AI.infer(messages, f"{section.folder}/revision_{rev}.md")
            section.script.update_from_script_markdown(response)
            return response

        return {
            section.script.title: _revise_section(section)
            for section in self.content.root.children
        }

    def smooth_transitions(self) -> List[str]:
        nodes = self.content.clean_nodes
        ret = []
        for prev, next in zip(nodes[:-1], nodes[1:]):
            last_paragraph = prev.script.content.split("\n\n")[-1]
            first_paragraph = next.script.content.split("\n\n")[0]
            messages = Config.prompts.transition.format_messages(
                previous_paragraph=last_paragraph,
                next_paragraph=first_paragraph,
            )
            response = AI.infer(messages, f"{next.folder}/transition.md")
            paragraphs = response.split("\n\n")
            while len(paragraphs) != 2:
                response = AI.infer(
                    messages, f"{next.folder}/transition.md", reuse=False
                )
                paragraphs = response.split("\n\n")
            new_last_paragraph = paragraphs[0].strip()
            new_first_paragraph = paragraphs[1].strip()
            prev.script.content = prev.script.content.replace(
                last_paragraph, new_last_paragraph
            )
            next.script.content = next.script.content.replace(
                first_paragraph, new_first_paragraph
            )
            ret.append(response)
        return ret
