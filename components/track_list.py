import pandas as pd
import streamlit as st

def show(tracks):
    if tracks is None:
        st.info("No tracks found")
        return
    write_intro()
    show_table(tracks)
 
def write_intro():
    st.write("## Tracks digged")

def show_table(df):
    st.dataframe(
        df,
        column_config={
            "track_id": None,
            "start": st.column_config.TextColumn(
                "Time",
                help="Estimated timestamp of the track"
            ),
            "end": None,
            "title": st.column_config.TextColumn(
                "Track",
                help="Name of the track"
            ),
            "artist": st.column_config.TextColumn(
                "Artist",
                help="Artist of the track"
            ),
            "genre": None,
            "spotify_link": st.column_config.LinkColumn(
                "Spotify link",
                display_text="Link"
            ),
            "cover_art": st.column_config.ImageColumn(
                "Cover Art (preview)"
            )
        },
        hide_index=True,
        width=800
    )
