import os
import requests
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed

def split_audio(file_path, chunk_length_ms):
    audio = AudioSegment.from_file(file_path)
    chunks = []
    for start in range(0, len(audio), chunk_length_ms):
        print("writing chunk: " + str(start))
        chunk = audio[start:start + chunk_length_ms]
        chunks.append(chunk)
    return chunks


def save_chunk(chunk, chunk_number, output_dir):
    chunk_file = os.path.join(output_dir, f"chunk_{chunk_number}.mp3")
    chunk.export(chunk_file, format="mp3")
    return chunk_file


def send_audio_to_shazam(file_path, api_key):
    url = "https://shazam-song-recognition-api.p.rapidapi.com/recognize/file"
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "shazam-song-recognition-api.p.rapidapi.com",
        'Content-Type': "application/octet-stream"
    }

    with open(file_path, 'rb') as f:
        audio_data = f.read()

    response = requests.post(url, headers=headers, data=audio_data)
    return response.json()


def extract_track_info(response_json):
    track_info = []
    track_data = response_json.get('track', {})
    if track_data:
        track_name = track_data.get('title', 'Unknown Title')
        artist_name = track_data.get('subtitle', 'Unknown Artist')
        track_info.append(f"{artist_name} - {track_name}")
    return track_info


def process_chunk(chunk, chunk_number, output_dir, api_key):
    chunk_file = save_chunk(chunk, chunk_number, output_dir)
    result = send_audio_to_shazam(chunk_file, api_key)
    os.remove(chunk_file)
    return chunk_number, extract_track_info(result)


def process_audio_file(file_path, api_key, chunk_length_ms=60000, output_dir='chunks'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chunks = split_audio(file_path, chunk_length_ms)
    all_track_info = [None] * len(chunks)
    track_set = set()  # keep track of unique tracks

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_chunk, chunk, i, output_dir, api_key): i for i, chunk in enumerate(chunks)}

        for future in as_completed(futures):
            chunk_number, track_info = future.result()
            # Insert the result into the correct index in the list
            all_track_info[chunk_number] = track_info

    # Flatten the list and remove duplicates
    final_track_info = []
    track_set = set()  # to keep track of unique tracks
    for track_list in all_track_info:
        if track_list:
            for track in track_list:
                if track not in track_set:
                    track_set.add(track)
                    final_track_info.append(track)

    return final_track_info
