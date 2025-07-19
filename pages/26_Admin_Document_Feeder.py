# pages/26_Admin_Document_Feeder.py

import streamlit as st
import os
from datetime import datetime

FEEDER_DIR = "data/manual_feed"
os.makedirs(FEEDER_DIR, exist_ok=True)

st.set_page_config(page_title="📥 TARGA Admin Feed", layout="centered")

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

st.title("📥 Admin Document Feeder")

st.markdown("""
Upload PDFs, scanned books, or method files that contain relevant GC knowledge.
These will be used for AI-enhanced retrieval and explanation in future modules.
""")

uploaded = st.file_uploader("Upload PDF or Image-Based File", type=["pdf", "jpg", "png", "jpeg"])

if uploaded:
    filename = uploaded.name
    save_path = os.path.join(FEEDER_DIR, f"{datetime.now().strftime('%Y%m%d_%H%M')}_{filename}")
    with open(save_path, "wb") as f:
        f.write(uploaded.read())

    st.success(f"✅ Saved: {save_path}")
    st.info("This document is now staged for ingestion by the retrieval AI module (coming soon).")