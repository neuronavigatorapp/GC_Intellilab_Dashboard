# pages/23_TARGA_Report_Generator.py

import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="TARGA Diagnostic Report Generator", layout="centered")
st.title("📄 GC Diagnostic Report Generator")

DATA_DIR = "data/chromatograms"
LABELS_FILE = "data/training_labels.csv"
REPORTS_DIR = "data/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# 1️⃣ File selection
if not os.path.exists(LABELS_FILE):
    st.warning("No tagged chromatograms found.")
else:
    labels = pd.read_csv(LABELS_FILE)
    selected = st.selectbox("Choose a chromatogram to generate a report for:", labels["filename"].unique())

    if selected:
        label_row = labels[labels["filename"] == selected].iloc[0]
        csv_path = os.path.join(DATA_DIR, selected)

        st.subheader("📋 Report Preview")
        st.text(f"Filename: {selected}")
        st.text(f"Behavior Label: {label_row['label']}")
        st.text(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        st.markdown("---")
        st.subheader("📤 Generate Report File")

        if st.button("Generate Markdown Report"):
            output_path = os.path.join(REPORTS_DIR, selected.replace(".csv", ".md"))
            with open(output_path, "w") as f:
                f.write(f"## GC Diagnostic Report\n")
                f.write(f"**File:** {selected}\n")
                f.write(f"**Label:** {label_row['label']}\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            st.success(f"✅ Report saved to {output_path}")

        if os.path.exists(os.path.join(REPORTS_DIR, selected.replace(".csv", ".md"))):
            with open(os.path.join(REPORTS_DIR, selected.replace(".csv", ".md")), "r") as f:
                st.markdown("---")
                st.subheader("📄 Current Report Preview")
                st.code(f.read(), language="markdown")