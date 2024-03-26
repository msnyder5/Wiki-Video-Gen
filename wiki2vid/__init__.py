from wiki2vid.script import ScriptBuilder, ScriptNode
from wiki2vid.state import State
from wiki2vid.video import VideoGenerator


class Wiki2Vid:
    def __init__(self, wiki_url: str = ""):
        self.state = State(wiki_url)

    def get_script(self) -> ScriptNode:
        scripter = ScriptBuilder(self.state)
        return scripter.create_script()

    def create_video(self):
        video_generator = VideoGenerator(self.state)
        return video_generator.generate_video()
