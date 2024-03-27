from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.segment import Content


class SEOBuilder:
    def __init__(self, content: Content):
        self.content = content

    def build_seo(self) -> None:
        self.video_title()
        self.video_description()

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
