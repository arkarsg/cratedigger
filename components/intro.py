import streamlit as st

def intro():
    st.write("# CrateDigger 💿📦")

    st.markdown(
        """
        Stop commenting "ID?" on your favourite SoundClound and Youtube mixes

        ### How it works
        Simply upload a mix you have in `mp3` only *or* paste a link to a mix.
        We recommend `YouTube` and `SoundCloud` links. Other providers are not tested yet.
        
        CrateDigger then analyses and tries to find Track IDs for the *entire* mix 😎  

        ---
    """
    )