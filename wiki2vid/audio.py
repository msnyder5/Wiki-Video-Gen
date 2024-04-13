import gc
import os
import re
import time
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Union

from elevenlabs import VoiceSettings, save
from elevenlabs.client import ElevenLabs
from moviepy.editor import AudioFileClip, concatenate_audioclips
from openai import OpenAI
from openai.types.audio import Transcription
from pydub import AudioSegment, silence

from wiki2vid.config import Config
from wiki2vid.script import ScriptBuilder
from wiki2vid.segment import Content, SegmentNode

if TYPE_CHECKING:
    from wiki2vid import Wiki2Vid


class AudioBuilder:
    def __init__(self, wiki2vid: Wiki2Vid):
        self.base_folder = f"{wiki2vid.base_folder}/audio"
        self.script = wiki2vid.script_builder.script
        self.elevenlabs = ElevenLabs(
            api_key=os.getenv("ELEVENLABS_API_KEY"), timeout=300
        )
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def build_audio(self) -> None:
        self._create_audio()
        self._remove_silence()
        self._create_transcript()

    def _create_audio(self) -> None:
        # repeat check
        if os.path.exists(f"{self.base_folder}/raw.mp3"):
            print("Audio already exists.")
            return
        # create audio and save
        print("Calling ElevenLabs to create audio...")
        audio = self.elevenlabs.generate(
            text=self.script,
            voice="Liam",
            model="eleven_multilingual_v1",
            voice_settings=VoiceSettings(
                stability=0.3,
                similarity_boost=0.75,
            ),
        )
        save(audio, f"{self.base_folder}/raw.mp3")

    def _remove_silence(self, max_silence_msec: int = 500):
        # repeat check
        if os.path.exists(f"{self.base_folder}/audio.mp3"):
            print("Silence already removed.")
            return
        # load audio
        audio: AudioSegment = AudioSegment.from_file(f"{self.base_folder}/raw.mp3")
        # find nonsilent parts (parts with speech)
        nonsilent_parts = silence.detect_nonsilent(
            audio, min_silence_len=max_silence_msec, silence_thresh=-52
        )
        # create a new audio to populate with nonsilent parts
        processed_audio: AudioSegment = AudioSegment.silent(duration=0)
        # add each nonsilent part to the new audio with a silence padding
        for start, end in nonsilent_parts:
            processed_audio += audio[max(0, start - 25) : min(end + 25, len(audio))]
            processed_audio += AudioSegment.silent(duration=max_silence_msec)
        # save the processed audio
        processed_audio.export(f"{self.base_folder}/audio.mp3", format="mp3")

    def _create_transcript(self) -> None:
        # repeat check
        if not os.path.exists(f"{self.base_folder}/words.txt") and os.path.exists(
            f"{self.base_folder}/segments.txt"
        ):
            print("Transcript already exists.")
            with open(f"{self.base_folder}/words.txt") as f:
                self.word_timestamps = f.read().splitlines()
            with open(f"{self.base_folder}/segments.txt") as f:
                self.segment_timestamps = f.read().splitlines()
            return
        # create transcript
        transcription = self.openai.audio.transcriptions.create(
            model="whisper-1",
            file=Path(f"{self.base_folder}/output.mp3"),
            language="en",
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
        )
        if transcription.model_extra is None:
            return
        # save word level timestamps
        with open(f"{self.base_folder}/words.txt", "w") as f:
            for word in transcription.model_extra["words"]:
                if not (word_str := word.get("word")):
                    continue
                if not (start := word.get("start")):
                    start = 0.0
                format_str = f"[{start:.2f}] {word_str}"
                self.word_timestamps.append(format_str)
                f.write(f"{format_str}\n")
        # save segment level timestamps
        with open(f"{self.base_folder}/segments.txt", "w") as f:
            for segment in transcription.model_extra["segments"]:
                if not (text := segment.get("text")):
                    continue
                if not (start := segment.get("start")):
                    start = 0.0
                format_str = f"[{start:.2f}] {text}"
                self.segment_timestamps.append(format_str)
                f.write(f"{format_str}\n")
