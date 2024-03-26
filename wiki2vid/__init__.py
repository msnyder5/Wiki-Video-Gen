from wiki2vid.config import Config
from wiki2vid.scripter import Scripter
from wiki2vid.scripter.outliner import Script
from wiki2vid.state import State
from wiki2vid.video import VideoGenerator
from wiki2vid.wiki import Wiki


class Wiki2Vid:
    def __init__(self, wiki_url: str = ""):
        self.state = State(wiki_url)

    def get_script(self) -> Script:
        scripter = Scripter(self.state)
        return scripter.create_script()

    def create_video(self):
        script = self.get_script()
        video_generator = VideoGenerator(self.state)
        return video_generator.generate_video()
