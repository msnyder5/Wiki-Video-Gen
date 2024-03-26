from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.script.script import ScriptNode
from wiki2vid.state import State


class ScriptBuilder:
    def __init__(self, state: State):
        self.state = state

    def create_script(self) -> ScriptNode:
        self._brainstorm()
        self._write_outline()
        self._write_sections()
        return self.state.script

    def _brainstorm(self) -> None:
        messages = [
            SystemMessage(
                content=Config.prompts.outline.brainstorm, name="Instructions"
            ),
            HumanMessage(content=self.state.wiki.content, name="Wiki Page Content"),
        ]
        self.state.brainstorm = AI.infer(messages, "brainstorming.md")

    def _write_outline(self) -> None:
        messages = [
            SystemMessage(content=Config.prompts.outline.write, name="Instructions"),
            HumanMessage(content=self.state.wiki.content, name="Wiki Page Content"),
            AIMessage(content=self.state.brainstorm, name="Brainstorming Results"),
        ]
        response = AI.infer(messages, "outline.md")
        self.state.script.update_from_outline_markdown(response)

    def _write_sections(self) -> None:
        def _write_section(section: ScriptNode) -> None:
            if section.children:
                messages = [
                    SystemMessage(
                        content=Config.prompts.section.write, name="Instructions"
                    ),
                    HumanMessage(
                        content=self.state.wiki.content, name="Wiki Page Content"
                    ),
                    HumanMessage(
                        content=section.outline_info,
                        name="Section Outline/Specification",
                    ),
                ]
            else:
                for child in section.children:
                    _write_section(child)
                child_scripts = section.children_script
                messages = [
                    SystemMessage(
                        content=Config.prompts.section.write_with_children,
                        name="Instructions",
                    ),
                    HumanMessage(
                        content=self.state.wiki.content, name="Wiki Page Content"
                    ),
                    HumanMessage(content=child_scripts, name="Children"),
                    HumanMessage(
                        content=section.outline_info,
                        name="Section Outline/Specification",
                    ),
                ]
            section.content = AI.infer(messages, section.filepath)

        for section in self.state.script.children:
            _write_section(section)

    # Only meant to be called on root node
    def _revise_sections(self) -> None:
        def _section_feedback(section: ScriptNode) -> str:
            messages = [
                SystemMessage(
                    content=Config.prompts.section.feedback, name="Instructions"
                ),
                HumanMessage(content=section.script, name="Section"),
            ]
            return AI.infer(messages, section.filepath)

        def _revise_section(section: ScriptNode) -> None:
            feedback_messages = [
                HumanMessage(content=_section_feedback(section), name="Feedback")
                for _ in range(Config.num_feedbacks)
            ]
            messages = [
                SystemMessage(
                    content=Config.prompts.section.revise, name="Instructions"
                ),
                HumanMessage(content=section.script, name="Section"),
                *feedback_messages,
            ]
            response = AI.infer(messages, section.filepath)
            section.update_from_script_markdown(response)

        for section in self.state.script.children:
            _revise_section(section)
