import asyncio
import io
from utils import process, AudioDownloader, AudioFileProcessor
from components import track_form as tf

request = tf.TracksRequest(
        url="https://soundcloud.com/wildpearlradio/wild-pearl-radio-metal_upa",
        scan_freqeuncy=60
    )
file : bytes = AudioDownloader().download(request.url)

async def run_profile_high_mem():
    await process(io.BytesIO(file), chunk_length_ms=300000)
    
async def run_profile():
    await AudioFileProcessor(file=io.BytesIO(file), chunk_length_in_seconds=600).process()
    
asyncio.run(run_profile())