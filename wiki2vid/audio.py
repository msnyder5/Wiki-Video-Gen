import os
import time
from typing import Iterator, Union

from elevenlabs import VoiceSettings, save
from elevenlabs.client import ElevenLabs
from moviepy.editor import AudioFileClip, concatenate_audioclips
from pydub import AudioSegment

from wiki2vid.config import Config
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
            node.audio_duration = AudioFileClip(audio_path).duration

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

    def _build_concat_audio(self):
        audio_clips = [
            AudioFileClip(f"{node.folder}/audio.mp3").duration
            for node in self.content.clean_nodes
        ]
        concatenated_audio = concatenate_audioclips(audio_clips)
        concatenated_audio.write_audiofile(f"{Config.folder}output.mp3")
