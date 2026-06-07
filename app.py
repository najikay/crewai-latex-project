"""
app.py
======
Streamlit UI for NavigatorCrew.
"""

import streamlit as st
from src.crew import build_crew
from src.config import logger

st.set_page_config(page_title="NavigatorCrew", layout="wide")

st.title("🦇 NavigatorCrew")
st.subheader("Biomimetic Navigation Research Platform")

tab1, tab2, tab3 = st.tabs(["Run Research", "Token Report", "Outputs"])

with tab1:
    if st.button("Start Research"):
        with st.spinner("Crew is working..."):
            crew, accountant = build_crew()
            result = crew.kickoff()
            accountant.finalize(crew.usage_metrics)
            accountant.save_report("outputs/token_report.md")
            st.success("Research Complete!")
            st.markdown(result)

with tab2:
    st.info("Run research to see token accounting.")

with tab3:
    st.info("Output files will appear here.")
