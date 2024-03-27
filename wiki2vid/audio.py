import os
import time
from typing import Iterator, Union

from elevenlabs import VoiceSettings, save
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

from wiki2vid.segment import Content, SegmentNode


class AudioBuilder:
    def __init__(self, content: Content):
        self.content = content
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def build_audio(self) -> None:
        for node in self.content.clean_nodes:
            audio_path = f"{node.folder}/audio.mp3"
            if not os.path.exists(audio_path):
                audio = self._build_segment_audio(node)
                save(audio, audio_path)
            node.audio_duration = self._get_audio_duration(audio_path)

    def _build_segment_audio(
        self, segment: SegmentNode
    ) -> Union[bytes, Iterator[bytes]]:
        return self.client.generate(
            text=segment.script.self_script.split("\n", 1)[1],
            voice="Liam",
            model="eleven_multilingual_v1",
            voice_settings=VoiceSettings(
                stability=0.3,
                similarity_boost=0.75,
            ),
        )

    def _get_audio_duration(self, audio_path: str) -> float:
        # audio_path = os.path.abspath(audio_path)
        # print(audio_path)
        # audio = MPyg123Player(audio_path)
        # time.sleep(10)
        audio = AudioSegment.from_file(audio_path, format="mp3")
        print(len(audio) / 1000.0)
        return len(audio) / 1000.0
