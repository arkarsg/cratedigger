import streamlit as st
from components import intro, track_form as tp, track_list
from utils import querier, ShazamAPI
from tracks_exceptions import InvalidUrlException, TooManySourceException, NoSourceException 
import asyncio

async def run():
    intro.intro()
    trax = tp.Form()
    submitted = trax.display_form()
    if submitted:
        data = trax.get_form_data()
        try:
            with st.status("Digging for tracks...", expanded=True) as s:
                querier.validate_data(data)
                result = await querier.query_tracks(data)
                s.update(label="Done", expanded=False, state='complete')
            track_list.show(result)
        except InvalidUrlException as i:
            st.error(i.message)
        except TooManySourceException as t:
            st.error(t.message)
        except NoSourceException as n:
            st.error(n.message)