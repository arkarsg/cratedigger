import asyncio
import io
from pydub import AudioSegment
from . import ShazamAPI, TrackStorage
import streamlit as st

def split_audio(file_path, chunk_length_ms):
    audio = AudioSegment.from_file(file_path)
    chunks = []
    for start in range(0, len(audio), chunk_length_ms):
        chunk = audio[start:start + chunk_length_ms]
        chunks.append((chunk, start, start+chunk_length_ms))
    return chunks

async def process(file, chunk_length_ms=60000):
    track_store = TrackStorage()
    api = ShazamAPI()

    def worker_wrapper(chunk):
        return worker(chunk, track_store, api)

    st.write("Splitting audio into chunks")
    chunks = split_audio(file, chunk_length_ms)
    st.write("Split audio into chunks")

    prog = 0
    prog_diff = 100 // len(chunks)
    bar = st.progress(prog, text="Analysing chunks...")
    async with api:
        tasks = [worker_wrapper(chunk) for chunk in chunks]
        for task in asyncio.as_completed(tasks):
            await task
            prog += prog_diff
            bar.progress(prog, text="Analysing chunks...")
    bar.progress(100, text="All chunks read")
    return await track_store.get_tracks()


async def worker(chunk, track_store, api):
    chunk_bytes, start, end = chunk
    buffer = io.BytesIO()
    chunk_bytes.export(buffer, format="mp3")
    track = await api.get_track_from_chunk(buffer)
    if track:
        await track_store.add_track(track=track, start_offset=start, end_offset=end)
    return

