import streamlit as st
from components import intro, track_form as tp, track_list, notice as nt
from utils import querier, ShazamAPI
from tracks_exceptions import InvalidUrlException, TooManySourceException, NoSourceException, MixTooBigException 
import time

async def run():
    limit_status = await check_api_limits()
    should_run = True
    if limit_status:
        if limit_status == "hourly":
            should_run = False
            nt.notify_rate_limit()
        elif limit_status == "monthly":
            should_run = False
            nt.notify_plan_limit()
    await app(should_run=should_run)

async def check_api_limits():
    async with ShazamAPI() as s:
        rate_limit_remainder, free_plan_remainder = await s.ping()
    if rate_limit_remainder == 0:
        return "hourly"
    if free_plan_remainder == 0:
        return "monthly"
    return None 

async def app(should_run):
    intro.intro()
    trax = tp.Form()
    submitted = trax.display_form(should_run)
    if submitted:
        data = trax.get_form_data()
        try:
            with st.status("Digging for tracks...", expanded=True) as s:
                querier.validate_data(data)
                start = time.time()
                result = await querier.query_tracks(data)
                end = time.time()
                s.update(label="Done", expanded=False, state='complete')
            st.success(f"Found tracks in {end - start:.{1}f} seconds")
            track_list.show(result)
        except MixTooBigException as m:
            s.update(label=m.message, expanded=False, state='error')
        except InvalidUrlException as i:
            st.error(i.message)
        except TooManySourceException as t:
            st.error(t.message)
        except NoSourceException as n:
            st.error(n.message)
    