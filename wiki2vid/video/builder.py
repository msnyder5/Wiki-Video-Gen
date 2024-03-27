from typing import Dict, List

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.segment import Content


class VideoBuilder:
    def __init__(self, content: Content):
        self.content = content

    def build_video(self) -> str:
        self.video_title()
        self.video_description()
        self.footage_search_terms()
        return "TODO: video filepath"

    def video_title(self) -> str:
        messages = Config.prompts.video_title.format_messages(
            script=self.content.script
        )
        response = AI.infer(messages, f"{Config.folder}/title.md")
        self.content.title = response.removeprefix('"').removesuffix('"')
        return response

    def video_description(self) -> str:
        messages = Config.prompts.video_description.format_messages(
            script=self.content.script
        )
        response = AI.infer(messages, f"{Config.folder}/description.md")
        self.content.description = response
        return response

    def footage_search_terms(self) -> Dict[str, List[str]]:
        ret = dict()
        for node in self.content.clean_nodes:
            messages = Config.prompts.footage.format_messages(
                section_content=node.script.self_script
            )
            response = AI.infer(messages, f"{node.folder}/search_terms.md")
            node.search_terms = [
                term.removeprefix("-").strip() for term in response.split("\n")
            ]
            ret[node.script.title] = node.search_terms
        return ret
