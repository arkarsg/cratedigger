import streamlit as st
from components import intro, track_form as tp, track_list
from utils import querier
from tracks_exceptions import TracksQueryException as e


def run():
    intro.intro()
    trax = tp.Form()
    submitted = trax.display_form()
    if submitted:
        data = trax.get_form_data()
        try:
            result = querier.query_tracks(data)
            track_list.show(result)
        except (e.TracksQueryException, NotImplementedError) as t:
            st.error(t)
