import pandas as pd
import streamlit as st

def show(tracks):
    st.write("## Tracks fished 🎣")
    df = pd.DataFrame([flatten_track(track) for track in tracks])
    df['start'] = pd.to_datetime(df['start'],
             unit='ms').dt.strftime('%H:%M:%S')
    df['end'] = pd.to_datetime(df['end'],
             unit='ms').dt.strftime('%H:%M:%S')

    st.dataframe(
        df,
        column_config={
            "track_id": None,
            "title": st.column_config.TextColumn(
                "Track",
                help="Name of the track"
            ),
            "artist": st.column_config.TextColumn(
                "Artist",
                help="Artist of the track"
            ),
            "genre": st.column_config.TextColumn(
                "Genre",
                help="Genre of the track"
            ),
            "spotify_link": st.column_config.LinkColumn(
                "Spotify link",
                display_text="Link"
            ),
            "cover_art": st.column_config.ImageColumn(
                "Cover Art (preview)"
            )
        },
        hide_index=True,
    )

def flatten_track(track):
    track_dict =  {
        "start": track.start_offset,
        "end": track.end_offset,
    }
    res = {**track_dict, **track.track.__dict__}
    return res