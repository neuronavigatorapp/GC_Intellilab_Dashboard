# pages/19_TARGA_Learning.py

import streamlit as st

st.set_page_config(page_title="TARGA Learning", layout="centered")

st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem;
    }
    label, textarea, input, select {
        font-size: 0.95rem !important;
    }
    @media screen and (max-width: 600px) {
        h1, h2, h3 {
            font-size: 1.4rem !important;
        }
        button[kind="primary"] {
            font-size: 1rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("📘 TARGA Learning Console")

st.markdown("""
Welcome to your on-demand GC school. These micro-lessons are designed to help you learn quickly, with ADHD-friendly summaries and optional quizzes.
""")

LESSONS = {
    "Intro to Gas Chromatography": "GC separates volatile compounds using a carrier gas and a temperature-controlled column.",
    "FID Basics": "Flame Ionization Detectors respond to carbon-containing compounds by producing ions in a hydrogen flame.",
    "Tailing Causes": "Peak tailing can result from column overloading, active sites, or poor injection technique.",
    "Backflush Logic": "Backflushing directs heavier compounds out of the system post-run, preventing contamination of the column or detector.",
    "Split Ratio Impact": "Changing the split ratio affects sample amount entering the column — higher splits mean less sample, better peak shape."
}

st.subheader("📚 Lesson Topics")
selected = st.selectbox("Select a Lesson", list(LESSONS.keys()))
st.info(LESSONS[selected])

if st.button("Take Quiz"):
    st.warning("🧪 Quiz feature coming soon!")