import streamlit as st

@st.dialog("Hourly limit reached", width="large")
def notify_rate_limit():
    st.write(
        """
        ### Hey there!
        We have reached the maximum number of music identification requests allowed
        for our free service tier at this hour.
        
        This means that we are temporarily unable to identify new tracks from DJ mixes.
        
        **Please try again in the next hour**

        Thank you for your understanding and the overwhelming support!
        """
    )
    
@st.dialog("Monthly Plan limit reached", width="large")
def notify_plan_limit():
    st.write(
        """
        ### Hey there!
        We have reached the maximum number of music identification requests allowed
        for our free service tier.
        
        This means that we are temporarily unable to identify new tracks from DJ mixes.
        
        **Please try again in the following month**

        Thank you for your understanding and the overwhelming support!
        """
    )