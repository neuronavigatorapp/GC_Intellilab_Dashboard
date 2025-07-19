# pages/25_AutoRetrain_Model.py

import streamlit as st
from models.train_classifier import train_model
import os

st.set_page_config(page_title="🔁 Retrain Model", layout="centered")
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
