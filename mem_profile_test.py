import asyncio
import io
from utils import process, AudioDownloader, AudioFileProcessor

url="https://soundcloud.com/wildpearlradio/wild-pearl-radio-metal_upa"
file : bytes = AudioDownloader().download(url)

async def run_profile_high_mem():
    await process(io.BytesIO(file), chunk_length_ms=600*1000)
    
async def run_profile():
    await AudioFileProcessor(file=io.BytesIO(file), chunk_length_in_seconds=600).process()
    
asyncio.run(run_profile())            # memory optimised
# asyncio.run(run_profile_high_mem())   # unoptimised