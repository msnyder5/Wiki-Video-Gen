from wiki2vid.audio import AudioBuilder
from wiki2vid.script import ScriptBuilder
from wiki2vid.segment import Content
from wiki2vid.video import VideoBuilder


class Wiki2Vid:
    def __init__(self, wiki_url: str = ""):
        self.content = Content(wiki_url)

    def build_script(self) -> None:
        script_builder = ScriptBuilder(self.content)
        script_builder.create_script()

    def build_audio(self) -> None:
        audio_builder = AudioBuilder(self.content)
        audio_builder.build_audio()

    def build_video(self) -> str:
        video_builder = VideoBuilder(self.content)
        return video_builder.build_video()

    def run(self) -> str:
        self.build_script()
        self.build_audio()
        return self.build_video()
