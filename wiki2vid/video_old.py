from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import requests
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips

from wiki2vid.ai import AI
from wiki2vid.config import Config
from wiki2vid.segment import Content, SegmentNode


class VideoBuilder:
    def __init__(self, content: Content):
        self.content = content

    def build_video(self) -> None:
        self.download_clips()
        self.stitch_clips()
        self.combine_segments()

    def download_clips(self):
        print("Downloading clips...")
        for node in self.content.clean_nodes:
            search_terms = self._search_terms(node)
            duration, i = self._existing_duration(node.folder)
            if duration >= node.audio_duration + 10:
                continue
            clips = {
                clip
                for term in search_terms
                for clip in Pexels.search(term)
                if clip.duration
            }
            while duration < node.audio_duration + 10:
                clip = clips.pop()
                clip_filepath = f"{node.folder}/clips/{i}.mp4"
                clip.download(clip_filepath)
                i += 1
                duration += clip.duration

    def stitch_clips(self):
        print("Stitching clips...")
        target_resolution = (1080, 1920)

        for node in self.content.clean_nodes:
            clip_folder = f"{node.folder}/clips"
            clip_files = sorted(
                [file for file in os.listdir(clip_folder) if file.endswith(".mp4")]
            )

            if not clip_files:
                continue  # No clips to process for this node

            # Load, resize, and concatenate clips
            clips = []
            for clip_file in clip_files:
                clip = VideoFileClip(
                    os.path.join(clip_folder, clip_file),
                    target_resolution=target_resolution,
                )
                clips.append(clip)

            concatenated_clip = concatenate_videoclips(clips, method="compose")

            # Trim concatenated clip to match audio duration
            if concatenated_clip.duration > node.audio_duration:
                concatenated_clip = concatenated_clip.subclip(0, node.audio_duration)

            # Add audio
            audio_file = f"{node.folder}/audio.mp3"
            narration_audio = AudioFileClip(audio_file)
            final_clip = concatenated_clip.set_audio(narration_audio)

            # Write the final video to a file
            output_file = f"{node.folder}/output.mp4"
            final_clip.write_videofile(output_file)

            # Close the clips to release resources
            for clip in clips:
                clip.close()
            narration_audio.close()

    def combine_segments(self):
        print("Combining segments...")
        segment_files = [
            f"{node.folder}/output.mp4" for node in self.content.clean_nodes
        ]
        output_file = f"{Config.folder}/output.mp4"
        segments = []
        for segment_file in segment_files:
            segments.append(VideoFileClip(segment_file))
        final_video = concatenate_videoclips(segments)
        final_video.write_videofile(output_file)
        for segment in segments:
            segment.close()

    @staticmethod
    def _existing_duration(folder: str) -> Tuple[float, int]:
        duration = 0
        i = 1
        if not os.path.exists(f"{folder}/clips"):
            return duration, i
        for file in os.listdir(f"{folder}/clips"):
            filepath = f"{folder}/clips/{file}"
            duration += VideoFileClip(filepath).duration
            i += 1
        return duration, i

    @staticmethod
    def _search_terms(node: SegmentNode) -> List[str]:
        messages = Config.prompts.footage.format_messages(
            section_content=node.script.self_script
        )
        response = AI.infer(messages, f"{node.folder}/search_terms.md")
        return [term.removeprefix("-").strip() for term in response.split("\n")]


class Pexels:
    SEARCH_ENDPOINT = "https://api.pexels.com/videos/search"
    GET_VIDEO_ENDPOINT = "https://api.pexels.com/videos/videos/{id}"
    HEADERS = {"Authorization": os.getenv("PEXELS_API_KEY")}

    @staticmethod
    def search(query: str) -> Set[PexelsClip]:
        print(f"Searching for {query}...")
        response = requests.get(
            Pexels.SEARCH_ENDPOINT,
            headers=Pexels.HEADERS,
            params={"query": query, "orientation": "landscape"},
        )
        clips = set()
        try:
            video_ids = [video["id"] for video in response.json()["videos"]]
        except KeyError:
            return clips
        for video_id in video_ids:
            try:
                response = requests.get(
                    Pexels.GET_VIDEO_ENDPOINT.format(id=video_id),
                    headers=Pexels.HEADERS,
                )
                data = response.json()
                clips.add(PexelsClip(data["video_files"][0]["link"], data["duration"]))
            except KeyError:
                continue
        return clips


@dataclass(frozen=True)
class PexelsClip:
    url: str
    duration: int

    def download(self, filepath: str):
        print("Downloading clip...")
        response = requests.get(self.url)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(response.content)
