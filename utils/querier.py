import streamlit as st
from tracks_exceptions import InvalidUrlException, NoSourceException, TooManySourceException
from io import BytesIO
from urllib.parse import urlparse
from .audio_downloader import AudioDownloader
from .audio_file_processor import AudioFileProcessor
import pandas as pd

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

def flatten_track(track):
    track_dict =  {
        "start": track.start_offset,
        "end": track.end_offset,
    }
    res = {**track_dict, **track.track.__dict__}
    return res

def df_adapter(tracks):
    if tracks:
        df = pd.DataFrame([flatten_track(track) for _, track in tracks])
        df = pd.DataFrame(tracks)
        df['start'] = pd.to_datetime(df['start'],
                unit='s').dt.strftime('%H:%M:%S')
        df['end'] = pd.to_datetime(df['end'],
                unit='s').dt.strftime('%H:%M:%S')
        df.sort_values(by=['start'], ascending=True, inplace=True)
        return df

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


