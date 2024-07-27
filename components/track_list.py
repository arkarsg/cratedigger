import pandas as pd
import streamlit as st

def show(tracks):
    st.write("## Tracks fished 🎣")
    tracks_table = pd.DataFrame(tracks, columns=["Title"])
    st.dataframe(data=tracks_table)