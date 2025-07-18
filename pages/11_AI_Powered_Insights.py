# pages/11_AI_Powered_Insights.py

import streamlit as st
from ai_modules.ollama_gc import ask_ollama

st.set_page_config(page_title="AI-Powered GC Insights", layout="wide")
st.title("🤖 AI-Powered GC Insights")

st.write("""
This page provides intelligent AI-driven insights for your GC data.  
Ask questions related to GC troubleshooting, method optimization, or general chromatographic data interpretation.
""")

user_question = st.text_area("Ask the AI about your GC data:", height=150)

if st.button("Get AI Response"):
    if user_question.strip() == "":
        st.warning("Please enter a question or request.")
    else:
        with st.spinner("Thinking..."):
            ai_response = ask_ollama(user_question)
            st.write("### AI Response:")
            st.success(ai_response)
