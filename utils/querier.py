import streamlit as st
from tracks_exceptions import InvalidUrlException, NoSourceException, TooManySourceException
from io import BytesIO
from urllib.parse import urlparse
from .audio_downloader import AudioDownloader
from .audio_file_processor import AudioFileProcessor

def query_tracks(tracks_request):
    if tracks_request.file:
        tracks = file_handler(
            tracks_request.file,
            tracks_request.scan_freqeuncy
        )
        return tracks
    if tracks_request.url:
        if not valid_url(tracks_request.url):
            raise InvalidUrlException
        tracks = link_handler(
            tracks_request.url,
            tracks_request.scan_freqeuncy
        )
        return tracks

async def file_handler(file, scan_freq):
    tracks = await AudioFileProcessor(file=file, chunk_length_in_seconds=scan_freq).process()
    return df_adapter(tracks)

async def link_handler(link, scan_freq):
    st.write("Pulling sound bytes...")
    ydl = AudioDownloader()
    file = ydl.download(link)
    st.write("Retrieved sound bytes!")
    tracks = await AudioFileProcessor(BytesIO(file), chunk_length_in_seconds=scan_freq).process()
    return df_adapter(tracks)

def df_adapter(tracks):
    if tracks:
        return [track for _, track in tracks] 
    
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


