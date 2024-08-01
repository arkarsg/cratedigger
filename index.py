from app import run
import streamlit as st
import asyncio
import psutil
import resource

if __name__ == "__main__":
    virtual_memory = psutil.virtual_memory()
    available_memory = virtual_memory.available
    memory_limit = int(available_memory * 0.98)
    # Set the memory limit
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
    
    st.set_page_config(
        page_title="CrateDigger",
        page_icon="🐡",
    )

    asyncio.run(run())
    
    