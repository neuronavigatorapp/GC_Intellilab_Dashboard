# pages/22_TARGA_Builder.py

import streamlit as st
import pandas as pd
import os
from datetime import datetime

BUILDER_CSV = "data/gc_builds.csv"
os.makedirs("data", exist_ok=True)

st.set_page_config(page_title="TARGA Builder Toolkit", layout="centered")

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

st.title("🛠 GC Build Documentation Toolkit")

st.markdown("""
Use this form to document any GC systems you've built from scratch, modified, or customized.
This creates a permanent build record for future reference or onboarding.
""")

# 1️⃣ Form to submit build
with st.form("build_form"):
    name = st.text_input("System Name / Nickname", placeholder="e.g. GC-08 - Reformate 2 Stream")
    serial = st.text_input("Instrument Serial Number")
    detectors = st.multiselect("Detectors Installed", ["FID", "TCD", "SCD", "ECD", "Methanizer"])
    methods = st.multiselect("Supported Methods", [
        "D1945", "D2163", "D2712", "D6730", "D7423", "D7833", "D5504", "D5441", "D7011", "Other"
    ])
    notes = st.text_area("Build Notes", placeholder="Include column layout, valve timings, flow paths, unique features...")
    submit = st.form_submit_button("Save Build")

if submit:
    row = pd.DataFrame([{
        "name": name,
        "serial": serial,
        "detectors": ", ".join(detectors),
        "methods": ", ".join(methods),
        "notes": notes,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }])

    if os.path.exists(BUILDER_CSV):
        existing = pd.read_csv(BUILDER_CSV)
        updated = pd.concat([existing, row], ignore_index=True)
    else:
        updated = row

    updated.to_csv(BUILDER_CSV, index=False)
    st.success("✅ Build saved.")

# 2️⃣ Show saved builds
if os.path.exists(BUILDER_CSV):
    st.markdown("---")
    st.subheader("📘 Build Records")
    df = pd.read_csv(BUILDER_CSV)
    st.dataframe(df, use_container_width=True)