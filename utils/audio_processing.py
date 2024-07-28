import io
import requests
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed
from .models import Track, ShazamAPI, TrackStorage 
     
api = ShazamAPI()
track_store = TrackStorage()
           
def split_audio(file_path, chunk_length_ms):
    audio = AudioSegment.from_file(file_path)
    chunks = []
    for start in range(0, len(audio), chunk_length_ms):
        chunk = audio[start:start + chunk_length_ms]
        chunks.append((chunk, start, start+chunk_length_ms))
    return chunks

def process(file, chunk_length_ms=60000):
    chunks = split_audio(file, chunk_length_ms)
    with ThreadPoolExecutor() as executor:
        executor.map(worker, chunks)
    return track_store.get_tracks()
    
def worker(chunk):
    chunk_bytes, start, end = chunk
    buffer = io.BytesIO()
    chunk_bytes.export(buffer, format="mp3")
    track = api.get_track_from_chunk(buffer)
    track_store.add_track(track=track, start_offset=start, end_offset=end)
    return
    

def send_audio_to_shazam(chunk, api_key):
    url = "https://shazam-song-recognition-api.p.rapidapi.com/recognize/file"
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "shazam-song-recognition-api.p.rapidapi.com",
        'Content-Type': "application/octet-stream"
    }
    buffer = io.BytesIO()
    chunk.export(buffer, format="mp3")
    response = requests.post(url, headers=headers, data=buffer)
    return response.json()


def extract_track_info(response_json):
    track_data = response_json.get('track', {})
    if track_data:
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
            title=track_name,
            artist=artist_name,
            spotify_link=spotify_link,
            genre=track_genre,
            cover_art=cover_art
        )
    return None


def process_chunk(chunk, chunk_number, api_key):
    result = send_audio_to_shazam(chunk, api_key)
    return chunk_number, extract_track_info(result)


def process_audio_file(file_path, api_key, chunk_length_ms=60000):
        chunks = split_audio(file_path, chunk_length_ms)
        all_track_info = [None] * len(chunks)
        track_set = set()  # keep track of unique tracks

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_chunk, chunk, i, api_key): i for i, chunk in enumerate(chunks)}

            for future in as_completed(futures):
                chunk_number, track_info = future.result()
                all_track_info[chunk_number] = track_info

        final_track_info = []
        for track in all_track_info:
                if track:
                    if track not in track_set:
                        track_set.add(track)
                        final_track_info.append(track)
        return final_track_info
