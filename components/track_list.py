import pandas as pd
import streamlit as st

def show(tracks):
    tracks_table = pd.DataFrame(tracks, columns=["Title"])
    st.dataframe(data=tracks_table)