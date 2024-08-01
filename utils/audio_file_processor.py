import asyncio
import io
import math
from pydub import AudioSegment
from . import ShazamAPI, TrackStorage
import streamlit as st
import soundfile as sf

class AudioFileProcessor:
    def __init__(self, file: io.BytesIO, chunk_length_in_seconds: int) -> None:
        self.file = file
        self.audio_file = sf.SoundFile(self.file)
        self.chunk_length = chunk_length_in_seconds
        self.audio_length_seconds = self.audio_file.frames / self.audio_file.samplerate
        self.api = ShazamAPI()
        self.track_storage = TrackStorage()
        
    async def process(self):
        async with self.api:
            tasks = [
                self._worker(start, start+self.chunk_length)
                for start in range(0, math.ceil(self.audio_length_seconds), self.chunk_length)
            ]
            for task in asyncio.as_completed(tasks):
                await task
        return

    async def _worker(self, start_time, stop_time):
        mp3_chunk = self._get_mp3_buffer_from_chunk(start_time, stop_time)
        track = await self.api.get_track_from_chunk(mp3_chunk)
        if track:
          await self.track_storage.add_track(track=track, start_offset=start_time, end_offset=stop_time)
        return

    def _get_mp3_buffer_from_chunk(self, start_time, stop_time):
        audio_section, sample_rate = self._read_audio_section(start_time, stop_time)
        mp3 = AudioSegment(
            audio_section.astype("float32").tobytes(),
            frame_rate=sample_rate,
            sample_width=audio_section.dtype.itemsize,
            channels=1
        )
        buffer = io.BytesIO()
        mp3.export(buffer, format="mp3", bitrate="128k")
        return buffer

    def _read_audio_section(self, start_time, stop_time):
        can_seek = self.audio_file.seekable()
        if not can_seek:
            raise ValueError("Not compatible with seeking")

        sr = self.audio_file.samplerate
        start_frame = sr * start_time
        frames_to_read = sr * (stop_time - start_time)
        self.audio_file.seek(start_frame)
        audio_section = self.audio_file.read(frames_to_read)
        return audio_section, sr
