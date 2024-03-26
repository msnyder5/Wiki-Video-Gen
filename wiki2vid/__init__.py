from wiki2vid.config import CONFIG
from wiki2vid.scripter import Scripter
from wiki2vid.scripter.outliner import Script
from wiki2vid.video import VideoGenerator
from wiki2vid.wiki import Wiki


class Wiki2Vid:
    def __init__(self, wiki_url: str = ""):
        self.wiki = Wiki(wiki_url or CONFIG.wiki_url)

    def get_script(self) -> Script:
        scripter = Scripter(self.wiki)
        return scripter.create_script()

    def create_video(self):
        script = self.get_script()
        video_generator = VideoGenerator(script)
        return video_generator.generate_video()
