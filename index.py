from app import run
import streamlit as st
import asyncio
import resource

if __name__ == "__main__":
    fixed_memory = 1 * 1024**3  # Streamlit limit 
    # Calculate 98% of the fixed memory value
    memory_limit = int(fixed_memory * 0.98)
    # Set the memory limit
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
    
    st.set_page_config(
        page_title="CrateDigger",
        page_icon="🐡",
    )

    asyncio.run(run())
    
    