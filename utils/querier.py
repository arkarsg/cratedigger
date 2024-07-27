from .audio_processing import process_audio_file
from tracks_exceptions import TracksQueryException as e
import streamlit as st
from io import BytesIO

def file_handler(file):
    return process_audio_file(file, api_key=st.secrets["api_key"])

def link_handler(link):
    raise NotImplementedError("Link handler not implemented")

def query_tracks(tracks_request):
    if tracks_request.file and tracks_request.url:
        raise e.TracksQueryException("Only provide a file or URL, not both.")
    if tracks_request.file:
        st.write(tracks_request.file.name)
        tracks = file_handler(
            BytesIO(tracks_request.file.getvalue())
        )
        return tracks
    if tracks_request.url:
        tracks = link_handler(tracks_request.url)
        return tracks
    raise e.TracksQueryException("Request made without file or URL")

