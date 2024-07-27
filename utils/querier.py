from .audio_processing import process_audio_file
from tracks_exceptions import InvalidUrlException, NoSourceException, TooManySourceException
import streamlit as st
from io import BytesIO
from urllib.parse import urlparse

def validate_data(tracks_request):
    if tracks_request.file and tracks_request.url:
        raise TooManySourceException
    if not tracks_request.file and not tracks_request.url:
        raise NoSourceException
    
def valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def file_handler(file, scan_freq):
    return process_audio_file(file, api_key=st.secrets["api_key"], chunk_length_ms=scan_freq * 1000)

def link_handler(link):
    raise NotImplementedError("Link handler not implemented")

def query_tracks(tracks_request):
    if tracks_request.file:
        tracks = file_handler(
            BytesIO(tracks_request.file.getvalue()),
            tracks_request.scan_freqeuncy
        )
        return tracks
    if tracks_request.url:
        if not valid_url(tracks_request.url):
            raise InvalidUrlException
        tracks = link_handler(tracks_request.url)
        return tracks

