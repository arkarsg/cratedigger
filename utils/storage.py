import threading

from utils.models import MixTrack, Track

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