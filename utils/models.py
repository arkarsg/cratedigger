import asyncio
from dataclasses import dataclass, field
import io
from typing import Any, Dict, Optional
import aiohttp
import streamlit as st

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


class ShazamAPI:
    def __init__(self):
        self.url = "https://shazam-song-recognition-api.p.rapidapi.com/recognize/file"
        self.headers = {
            'x-rapidapi-key': st.secrets["api_key"],
            'x-rapidapi-host': "shazam-song-recognition-api.p.rapidapi.com",
            'Content-Type': "application/octet-stream"
        }
        self.session = None
        self.timeout = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        self.timeout = aiohttp.ClientTimeout(total=150)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def ping(self):
        async with self.session.post(url=self.url, headers=self.headers) as response:
            return self._check_limit(response)
            
    async def get_track_from_chunk(self, chunk: io.BytesIO) -> Optional[Track]:
        try:
            async with self.session.post(url=self.url, headers=self.headers, data=chunk, timeout=self.timeout) as response:
                limit = self._check_limit(response)
                if limit:
                    st.rerun()
                response.raise_for_status()
                resp_json = await response.json()
                return self._scan_track(resp_json)
        except aiohttp.ClientError as e:
            if e.status == 502:
                st.warning("Could not get track information")
            elif e.status == 400:
                st.warning("No track data found in chunk")
            elif e.status == 504:
                st.warning("You (working) ---> Gateway (working) ---> Server (took too long to respond)")
            else:
                st.warning("Could not get track information")
        return None

    def _check_limit(self, response):
        rate_limit_remainder = response.headers['X-RateLimit-Requests-Remaining']
        free_plan_remainder = response.headers['X-RateLimit-rapid-free-plans-hard-limit-Remaining']
        if int(rate_limit_remainder) <= 0:
            return "hourly"
        if int(free_plan_remainder) <= 0:
            return "monthly"
        return None  
        
    def _scan_track(self, resp: Dict[str, Any]) -> Optional[Track]:
        track_data = resp.get('track', {})
        if not track_data:
            return None

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

    async def close(self):
        if self.session:
            await self.session.close()
