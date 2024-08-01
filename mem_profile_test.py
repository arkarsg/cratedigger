from components import track_list
from utils import querier
from components import track_form as tf

async def run_profile():
    request = tf.TracksRequest(
        url="https://soundcloud.com/wildpearlradio/wild-pearl-radio-metal_upa?in=wildpearlradio/sets/jun-2024",
        scan_freqeuncy=180
    )
    result = await querier.query_tracks(request)
    track_list.show(result)