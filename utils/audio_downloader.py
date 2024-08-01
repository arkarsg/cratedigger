import io
import yt_dlp
from tracks_exceptions import MixTooBigException
from contextlib import redirect_stdout
from config import MAX_DURATION

class AudioDownloader:
    def __init__(self):
        self.opts = {
            'extractaudio':True,
            'format':'mp3/bestaudio/best',
            'noplaylist':True,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3'
                }
            ],
            'outtmpl':'-',
            'logtostderr': True
        }

    def download(self, link):
        buffer = io.BytesIO()
        with redirect_stdout(buffer), yt_dlp.YoutubeDL(self.opts) as ydl:
            metadata = ydl.extract_info(link, download=False)
            if metadata["duration"] >= MAX_DURATION:
                raise MixTooBigException
            ydl.download([link])
        return buffer.getvalue()