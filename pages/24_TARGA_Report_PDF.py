# pages/24_TARGA_Report_PDF.py

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="📑 PDF Diagnostic Export", layout="centered")

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

st.title("📑 Export GC Report to PDF")

LABELS_FILE = "data/training_labels.csv"
DATA_DIR = "data/chromatograms"
PDF_DIR = "data/reports"
os.makedirs(PDF_DIR, exist_ok=True)

if not os.path.exists(LABELS_FILE):
    st.warning("No labeled chromatograms found.")
else:
    labels_df = pd.read_csv(LABELS_FILE)
    options = labels_df["filename"].unique().tolist()
    selected = st.selectbox("Choose a chromatogram", options)

    if selected:
        row = labels_df[labels_df.filename == selected].iloc[0]

        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 14)
                self.cell(0, 10, "GC Diagnostic Report", ln=1, align="C")
                self.ln(5)

        if st.button("📥 Generate PDF Report"):
            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Filename: {row['filename']}", ln=1)
            pdf.cell(0, 10, f"Behavior Label: {row['label']}", ln=1)
            pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)

            path = os.path.join(PDF_DIR, selected.replace(".csv", ".pdf"))
            pdf.output(path)
            st.success(f"✅ PDF saved to: {path}")

            with open(path, "rb") as f:
                st.download_button(
                    label="📄 Download PDF",
                    data=f,
                    file_name=os.path.basename(path),
                    mime="application/pdf"
                )