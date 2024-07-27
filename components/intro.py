import streamlit as st

def intro():
    st.set_page_config(
        page_title="TraxFish",
        page_icon="🐡",
    )

    st.write("# TraxFish 🐡🔥")

    st.markdown(
        """
        Stop commenting "ID?" on your favourite SoundClound and Youtube mixes
        ### Key features
        - File upload
        - Link to DJ mix
        
        # Get started
        1. Upload your mix **or** insert a link to your mix
        2. Click "Find
    """
    )