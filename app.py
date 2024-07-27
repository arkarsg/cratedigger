import streamlit as st
from components import intro, track_form as tp, track_list
from utils import querier
from tracks_exceptions import InvalidUrlException, TooManySourceException, NoSourceException 

def run():
    intro.intro()
    trax = tp.Form()
    submitted = trax.display_form()
    if submitted:
        data = trax.get_form_data()
        try:
            querier.validate_data(data)
            with st.spinner(f"Fishing tracks from *{data.url or data.file.name}* every *{data.scan_freqeuncy} seconds*"):
                result = querier.query_tracks(data)
                track_list.show(result)
        except NotImplementedError:
            st.info("Feature coming soon!")
        except InvalidUrlException as i:
            st.error(i.message)
        except TooManySourceException as t:
            st.error(t.message)
        except NoSourceException as n:
            st.error(n.message)
