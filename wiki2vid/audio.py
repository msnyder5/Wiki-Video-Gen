import os

from elevenlabs.client import ElevenLabs

from wiki2vid.segment import Content


class AudioBuilder:
    def __init__(self, content: Content):
        self.content = content
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def build_audio(self) -> None:
        pass
