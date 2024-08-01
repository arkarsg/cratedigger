import asyncio
import io
import math
from pydub import AudioSegment 
from . import ShazamAPI, TrackStorage
import streamlit as st
import soundfile as sf
import gc

TEXT = "Analysing chunks...     *This might take a while*"
class AudioFileProcessor:
    def __init__(self, file: io.BytesIO, chunk_length_in_seconds: int) -> None:
        self.file = file 
        self.audio_file = sf.SoundFile(self.file)
        self.chunk_length = chunk_length_in_seconds
        self.audio_length_seconds = self.audio_file.frames / self.audio_file.samplerate
        self.api = ShazamAPI()
        self.track_storage = TrackStorage()
        
    async def process(self):
        n = self.audio_length_seconds // self.chunk_length
        prog = 0
        prog_delta = 100 // n
        bar = st.progress(prog, text=TEXT)

        async with self.api:
            tasks = [
                self._worker(start)
                for start in range(0, math.ceil(self.audio_length_seconds), self.chunk_length)
            ]
            for task in asyncio.as_completed(tasks):
                await task
                prog = int(min(100, prog + prog_delta))
                bar.progress(prog, text=TEXT)
        bar.progress(100, text="All chunks read!")
        return await self.track_storage.get_tracks()

    async def _worker(self, start_time):
        mp3_chunk = self._get_mp3_buffer_from_chunk(start_time)
        track = await self.api.get_track_from_chunk(mp3_chunk)
        if track:
          await self.track_storage.add_track(
              track=track,
              start_offset=start_time,
              end_offset=start_time + self.chunk_length)

    def _get_mp3_buffer_from_chunk(self, start_time):
        self.file.seek(0)
        mp3 = AudioSegment.from_file(
            file=self.file,
            start_second=start_time,
            duration=self.chunk_length,
            format="mp3"
        )
        buffer = io.BytesIO()
        mp3.export(buffer, format="mp3", bitrate="128k")
        del mp3
        gc.collect()
        return buffer
