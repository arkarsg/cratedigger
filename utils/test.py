import threading
from collections import defaultdict

class TrackInfo:
    def __init__(self, start_offset, end_offset):
        self.start_offset = start_offset
        self.end_offset = end_offset

    def update_offsets(self, start_offset, end_offset):
        self.start_offset = min(self.start_offset, start_offset)
        self.end_offset = max(self.end_offset, end_offset)

class ConcurrentSafeTrackStorage:
    def __init__(self):
        self._tracks = defaultdict(lambda: TrackInfo(float('inf'), float('-inf')))
        self._lock = threading.Lock()

    def add_track(self, track_id, start_offset, end_offset):
        with self._lock:
            if track_id in self._tracks:
                self._tracks[track_id].update_offsets(start_offset, end_offset)
            else:
                self._tracks[track_id] = TrackInfo(start_offset, end_offset)

    def get_tracks(self):
        with self._lock:
            # Convert dictionary to list of tuples (track_id, TrackInfo)
            tracks_list = list(self._tracks.items())
            # Sort the list by start_offset
            sorted_tracks = sorted(tracks_list, key=lambda item: item[1].start_offset)
            return sorted_tracks

# Example usage
storage = ConcurrentSafeTrackStorage()
storage.add_track("track1", 10, 20)
storage.add_track("track1", 5, 15)
storage.add_track("track2", 30, 40)
storage.add_track("track3", 0, 10)

tracks = storage.get_tracks()
for track_id, info in tracks:
    print(f"Track ID: {track_id}, Start: {info.start_offset}, End: {info.end_offset}")
