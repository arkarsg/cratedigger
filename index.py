from app import run
import streamlit as st
import asyncio

if __name__ == "__main__":
    st.set_page_config(
        page_title="CrateDigger",
        page_icon="🐡",
    )

    asyncio.run(run())