import asyncio
import threading

from utils.models import MixTrack, Track

class TrackStorage:
    def __init__(self):
        self._tracks = {}
        self._lock = asyncio.Lock()

    async def add_track(self, track: Track, start_offset: int, end_offset: int):
        async with self._lock:
            if track.track_id in self._tracks:
                print("track updated " + track.track_id)
                self._tracks[track.track_id].update_offsets(start_offset, end_offset)
            else:
                print("track added " + track.track_id)
                self._tracks[track.track_id] = MixTrack(start_offset, end_offset, track)

    async def get_tracks(self):
        async with self._lock:
            # Convert dictionary to list of tuples (track_id, MixTrack)
            tracks_list = list(self._tracks.items())
            return tracks_list