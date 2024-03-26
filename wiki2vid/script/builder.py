from typing import List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.script.script import Script, ScriptNode
from wiki2vid.state import State

TEST_OUTLINE = """
## Introduction
Bloodhound, the Technological Tracker, is a formidable Recon Legend in Apex Legends. Known for their unparalleled tracking skills, Bloodhound can reveal hidden enemies, traps, and clues, making them a vital asset to any team. They are the embodiment of the perfect hunter, blending the Old Ways with advanced technology to locate and eliminate their prey.

## Abilities

### Ultimate Ability: Beast of the Hunt
- Transforms Bloodhound into the ultimate hunter, enhancing their senses to see cold tracks and moving faster.
- Launches a White Raven towards the nearest enemy, with downed enemies causing additional White Ravens to spawn.
- Downing enemies extends the duration of the ability, with a base duration of 30 seconds.
- Increases speed by 30%, and highlights enemies in red, making it easier to see them even through smoke or gas.

### Tactical Ability: Eye of the Allfather
- Reveals enemies, traps, and clues through all structures in front of you in a 125� cone.
- Has a range of up to 75 meters and highlights detected enemies for you and your allies.
- Activation time is 1.8s, with a cooldown of 25 seconds.
- Exposes Bloodhound to detection but provides critical information on enemy positions.

### Passive Ability: Tracker
- Enemies leave behind clues that Bloodhound can see to track their movements.
- Clues include footprints, slide marks, and actions like door usage or gunfire, which disappear after 90 seconds.
- White Ravens may appear to guide Bloodhound to battle, charging their abilities when activated or scanned.

## Legend Upgrades
- Special perks available in Battle Royale modes, enhancing abilities as Bloodhound levels up their Evo Armor.
- Options include reducing the cooldown of Eye of the Allfather, making White Ravens grant more Beast of the Hunt charge, and others that enhance the effectiveness of Bloodhound's abilities.

## Conclusion
Bloodhound's mastery of tracking and reconnaissance makes them a powerhouse in Apex Legends. Their abilities allow teams to gain the upper hand by revealing enemy positions, setting up ambushes, or avoiding traps. Whether leading the charge with Beast of the Hunt or strategically using Eye of the Allfather to scan the battlefield, Bloodhound exemplifies the perfect synergy between the primal and the technological, proving that knowledge is power on the battlefield.
""".strip()

TEST_BRAINSTORM = """
- Intro
- Abilities
    - Ultimate Ability
    - Tactical Ability
    - Passive Ability
- Any other perks or unique features if applicable
- Conclusion
""".strip()


class ScriptBuilder:
    def __init__(self, state: State):
        self.state = state

    def create_script(self) -> Script:
        # self._brainstorm()
        self.state.brainstorm = TEST_BRAINSTORM
        # self._write_outline()
        self.state.script.root.update_from_outline_markdown(TEST_OUTLINE)
        self._write_sections()
        self._revise_sections()
        return self.state.script

    def _brainstorm(self) -> None:
        messages = Config.prompts.outline.brainstorm.format_messages(
            wiki_content=self.state.wiki.content
        )
        self.state.brainstorm = AI.infer(messages, f"{Config.folder}/brainstorming.md")

    def _write_outline(self) -> None:
        messages = Config.prompts.outline.write.format_messages(
            wiki_content=self.state.wiki.content, brainstorm=self.state.brainstorm
        )
        response = AI.infer(messages, f"{Config.folder}/outline.md")
        self.state.script.root.update_from_outline_markdown(response)

    def _write_sections(self) -> None:
        def _write_section(section: ScriptNode) -> None:
            if section.children:
                for child in section.children:
                    _write_section(child)
                # messages = Config.prompts.section.write_with_children.format_messages(
                #     wiki_content=self.state.wiki.content,
                #     section_outline=section.self_outline,
                #     children=section.children_script,
                # )
            else:
                messages = Config.prompts.section.write.format_messages(
                    wiki_content=self.state.wiki.content,
                    section_outline=section.self_outline,
                )
                section.content = AI.infer(messages, section.filename)

        for section in self.state.script.root.children:
            _write_section(section)

    def _revise_sections(self) -> None:
        def _section_feedbacks(section: ScriptNode) -> List[HumanMessage]:
            messages = Config.prompts.section.feedback.format_messages(
                section_content=section.content
            )
            feedbacks = [
                AI.infer(messages, f"{section.filepath}_feedback{i}.md")
                for i in range(Config.num_feedbacks)
            ]
            return [HumanMessage(content=feedback) for feedback in feedbacks]

        def _revise_section(section: ScriptNode) -> None:
            messages = Config.prompts.section.revise.format_messages(
                section_content=section.content
            ) + _section_feedbacks(section)
            response = AI.infer(messages, f"{section.filepath}_revision.md")
            section.update_from_script_markdown(response)

        for section in self.state.script.root.children:
            if section.children:
                for child in section.children:
                    if child.children:
                        for grandchild in child.children:
                            _revise_section(grandchild)
                    else:
                        _revise_section(child)
            else:
                _revise_section(section)
