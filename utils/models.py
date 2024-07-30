from dataclasses import dataclass, field
import io
import threading
import streamlit as st
import requests

@dataclass(frozen=True)
class Track:
    track_id: int = field(hash=True)
    title: str = field(hash=True)
    artist: str = field(hash=True)
    genre: str = field(hash=True)
    spotify_link: str = field(hash=False, compare=False)
    cover_art: str = field(hash=False, compare=False)

    def __eq__(self, value: object) -> bool:
        return self.track_id == value.track_id and \
                self.title == value.title and \
                self.artist == value.artist and \
                self.genre == value.genre

class MixTrack:
    def __init__(self, start_offset, end_offset, track):
        self.start_offset = start_offset
        self.end_offset = end_offset
        self.track = track

    def update_offsets(self, start_offset, end_offset):
        self.start_offset = min(self.start_offset, start_offset)
        self.end_offset = max(self.end_offset, end_offset)

class TrackStorage:
    def __init__(self):
        self._tracks = {}
        self._lock = threading.Lock()

    def add_track(self, track: Track, start_offset: int, end_offset: int):
        with self._lock:
            if track.track_id in self._tracks:
                print("track updated")
                self._tracks[track.track_id].update_offsets(start_offset, end_offset)
            else:
                print("track added" + track.track_id)
                self._tracks[track.track_id] = MixTrack(start_offset, end_offset, track)

    def get_tracks(self):
        with self._lock:
            # Convert dictionary to list of tuples (track_id, MixTrack)
            tracks_list = list(self._tracks.items())
            return tracks_list 


class ShazamAPI:
    def __init__(self):
        self.url = "https://shazam-song-recognition-api.p.rapidapi.com/recognize/file"
        self.headers = {
            'x-rapidapi-key': st.secrets["api_key"],
            'x-rapidapi-host': "shazam-song-recognition-api.p.rapidapi.com",
            'Content-Type': "application/octet-stream"
        }

    def get_track_from_chunk(self, chunk: io.BytesIO):
        response = requests.post(
            url=self.url,
            headers=self.headers,
            data=chunk
        )
        return self._scan_track(response.json())

    def _scan_track(self, resp):
        track_data = resp.get('track', {})
        if track_data:
            track_id = track_data.get('key', 'Unknown')
            track_name = track_data.get('title', 'Unknown Title')
            artist_name = track_data.get('subtitle', 'Unknown Artist')
            track_genre = track_data.get("genres", {}).get("primary", "Unknown Genre")
            spotify_link = None
            for provider in track_data.get("hub", {}).get("providers", []):
                if provider.get("type") == "SPOTIFY":
                    spotify_link = provider.get("actions", [{}])[0].get("uri", "No Spotify Link")
                    break
            cover_art = track_data.get("images", {}).get("coverart", "No Cover Art")
            return Track(
                track_id=track_id,
                title=track_name,
                artist=artist_name,
                spotify_link=spotify_link,
                genre=track_genre,
                cover_art=cover_art
            )
        return None

 