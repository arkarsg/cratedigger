import io
import yt_dlp
from contextlib import redirect_stdout

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

    def dowload(self, link):
        buffer = io.BytesIO()
        with redirect_stdout(buffer), yt_dlp.YoutubeDL(self.opts) as ydl:
            ydl.download([link])
        return buffer.getvalue()