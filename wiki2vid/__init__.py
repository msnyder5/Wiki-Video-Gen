from typing import Optional

from wiki2vid.audio import AudioBuilder
from wiki2vid.config import Config
from wiki2vid.script import ScriptBuilder
from wiki2vid.segment import Content, SegmentNode
from wiki2vid.seo import SEOBuilder
from wiki2vid.video import VideoBuilder
from wiki2vid.wiki import Wiki


class Wiki2Vid:
    def __init__(self, wiki_url: str = ""):
        self.base_folder = f"{Config.folder}/{wiki_url.split('/')[-1]}"
        self.wiki_url = wiki_url

        # Builders
        self.script_builder = ScriptBuilder(self)
        self.seo_builder = SEOBuilder(self)
        self.audio_builder = AudioBuilder(self)
        self.video_builder = VideoBuilder(self)

    def run(self) -> None:
        self.script_builder.build_script()
        self.seo_builder.build_seo()
        self.audio_builder.build_audio()
        self.video_builder.build_video()
