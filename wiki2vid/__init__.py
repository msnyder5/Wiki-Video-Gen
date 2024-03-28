from wiki2vid.audio import AudioBuilder
from wiki2vid.script2 import ScriptBuilder
from wiki2vid.segment import Content
from wiki2vid.seo import SEOBuilder
from wiki2vid.video import VideoBuilder


class Wiki2Vid:
    def __init__(self, wiki_url: str = ""):
        self.content = Content(wiki_url)

    def run(self) -> None:
        self.build_script()
        self.build_seo()
        self.build_audio()
        # self.build_video()

    def build_script(self) -> None:
        script_builder = ScriptBuilder(self.content)
        script_builder.create_script()

    def build_seo(self) -> None:
        seo_builder = SEOBuilder(self.content)
        seo_builder.build_seo()

    def build_audio(self) -> None:
        audio_builder = AudioBuilder(self.content)
        audio_builder.build_audio()

    def build_video(self) -> None:
        video_builder = VideoBuilder(self.content)
        video_builder.build_video()
