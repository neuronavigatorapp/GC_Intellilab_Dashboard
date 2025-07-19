# pages/17_CSV_Tagger.py

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="CSV Tagger", layout="centered")

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

st.title("📝 CSV Chromatogram Tagger")

UPLOAD_DIR = "data/chromatograms"
LABELS_CSV = "data/training_labels.csv"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

# 1️⃣ Upload CSV
uploaded_file = st.file_uploader("Upload Chromatogram CSV", type="csv")

if uploaded_file:
    filename = uploaded_file.name
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"Saved to: {file_path}")
    df = pd.read_csv(file_path)

    st.subheader("📈 Preview")
    st.line_chart(df.set_index(df.columns[0]))

    # 2️⃣ Label Selection
    label = st.selectbox("Select Behavior Label", [
        "Normal", "Tailing", "Fronting", "Ghost Peak", "Baseline Drift", "Noise", "Unknown"])

    if st.button("Save Label"):
        if os.path.exists(LABELS_CSV):
            label_df = pd.read_csv(LABELS_CSV)
        else:
            label_df = pd.DataFrame(columns=["filename", "label"])

        # Remove old label if exists
        label_df = label_df[label_df.filename != filename]
        label_df = pd.concat([label_df, pd.DataFrame([[filename, label]], columns=["filename", "label"])], ignore_index=True)
        label_df.to_csv(LABELS_CSV, index=False)
        st.success("✅ Label saved successfully.")