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
        with st.form(key="tracks_uploader"):
            self.url = st.text_input(
                label="Paste a link to your mix"
            )
            
            st.write("**OR**")

            self.file = st.file_uploader(
                label="Upload a mix",
                type=["mp3"],
                accept_multiple_files=False
            )
            
            self.scan_frequency = st.slider(
                label="Scan frequency",
                min_value=4,
                max_value=100
            )

            submitted = st.form_submit_button("Get track IDs")
            return submitted

    def get_form_data(self):
        return TracksRequest(file=self.file, url=self.url, scan_freqeuncy=self.scan_frequency)