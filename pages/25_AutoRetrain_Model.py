# pages/25_AutoRetrain_Model.py

import streamlit as st
from models.train_classifier import train_model
import os

st.set_page_config(page_title="🔁 Retrain Model", layout="centered")

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

st.title("🔁 One-Click Model Retraining")

st.markdown("""
Click the button below to retrain your chromatogram classification model using the most recent labeled data.
This will overwrite the previous model.
""")

if st.button("🔄 Retrain GC Classifier"):
    try:
        train_model()
        st.success("✅ Model retrained and saved to models/gc_fault_classifier.pkl")
    except Exception as e:
        st.error(f"Error during retraining: {e}")