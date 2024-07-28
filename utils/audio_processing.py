import io
import random
import requests
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed
from .models import Track, ShazamAPI, TrackStorage 
import streamlit as st
     
api = ShazamAPI()
           
def split_audio(file_path, chunk_length_ms):
    audio = AudioSegment.from_file(file_path)
    chunks = []
    for start in range(0, len(audio), chunk_length_ms):
        chunk = audio[start:start + chunk_length_ms]
        chunks.append((chunk, start, start+chunk_length_ms))
    return chunks

def process(file, chunk_length_ms=60000):
    with st.status("Digging tracks...", expanded=True) as s:
        track_store = TrackStorage()
        st.write("Splitting mix into chunks...")
        chunks = split_audio(file, chunk_length_ms)
        
        logs = st.empty()
        def worker_wrapper(chunk):
            return worker(chunk, track_store)

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(worker_wrapper, chunk): i for i, chunk in enumerate(chunks)}
            for _ in as_completed(futures):
                logs.text(random_message())

        s.update(
            label="Found tracks!", state="complete", expanded=False
        )
        return track_store.get_tracks()

def worker(chunk, track_store):
    chunk_bytes, start, end = chunk
    buffer = io.BytesIO()
    chunk_bytes.export(buffer, format="mp3")
    track = api.get_track_from_chunk(buffer)
    track_store.add_track(track=track, start_offset=start, end_offset=end)
    return

def random_message():
    msg = [
        "Wow, these are some esoteric tracks",
        "Going to the local vinyl store",
        "This fella's good",
        "Found some real grooooovy tunes",
        "Yep, still digging",
        "No, this is not stuck",
        "Lost in the sauce",
        "Yeah bro, this track is really indie",
        "Found this electric boogaloo",
        "Seriously, where did you find this"
    ]
    
    return random.choice(msg)
