import streamlit as st
from dataclasses import dataclass

@dataclass
class TracksRequest:
    file: any = None
    url: any = None
    scan_freqeuncy: any = None

class Form:
    def __init__(self) -> None:
        self.url = None
        self.file = None
        self.scan_frequency = None

    def display_form(self):
        with st.form(key="tracks_uploader", border=False):
            st.write("### 1. Upload **or** paste a link to your mix")
            with st.container(border=True):
                self.url = st.text_input(
                    label="Paste a link to your mix"
                )
            
                st.write("---")

                self.file = st.file_uploader(
                    label="Upload a mix",
                    type=["mp3"],
                    accept_multiple_files=False
                )
            st.write("### 2. Select *scan frequency*")
            with st.container(border=True):
                st.write(
                """
                *Scan frequency* lets you choose how often CrateDigger should
                try to identify a track in the mix.
                
                For mixes with fast transitions, a lower number is recommended (`<45s`).
                """
                )
                st.warning("Lower scan frequency may take longer to dig for tracks")
                self.scan_frequency = st.slider(
                    label="Scan frequency",
                    min_value=30,
                    max_value=60*3,
                    step=5
                )
            submitted = st.form_submit_button("Get track IDs")
            return submitted

    def get_form_data(self):
        return TracksRequest(file=self.file, url=self.url, scan_freqeuncy=self.scan_frequency)