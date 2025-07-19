# pages/18_AI_Chromatogram_Diagnosis.py

import streamlit as st
import pandas as pd
import plotly.express as px
from models.infer_classifier import classify_chromatogram

st.set_page_config(page_title="AI Chromatogram Diagnosis", layout="centered")

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

st.title("AI-Powered Chromatogram Diagnosis")

# 1️⃣ Upload CSV
st.markdown("""
Upload a chromatogram file to classify potential anomalies using your trained AI model.
""")

uploaded_file = st.file_uploader("Upload Chromatogram CSV", type="csv")

if uploaded_file:
    with open("data/temp_eval.csv", "wb") as f:
        f.write(uploaded_file.read())

    df = pd.read_csv("data/temp_eval.csv")
    st.subheader("📈 Preview Chromatogram")
    fig = px.line(df, x=df.columns[0], y=df.columns[1], labels={df.columns[0]: "Time (min)", df.columns[1]: "Signal"})
    st.plotly_chart(fig, use_container_width=True)

    try:
        label, confidence = classify_chromatogram("data/temp_eval.csv")
        st.success(f"🧠 Predicted Fault Type: **{label}**")
        st.info(f"Confidence Score: **{confidence:.2f}**")

        st.markdown("---")
        st.markdown("#### Diagnostic Feedback")

        feedback_map = {
            "Normal": "This run appears normal based on the signal shape and timing.",
            "Tailing": "Tailing may indicate column contamination, poor split ratio, or overloading.",
            "Fronting": "Fronting suggests injection overloading or inlet temperature too high.",
            "Ghost Peak": "Ghost peaks may result from sample carryover or injector contamination.",
            "Baseline Drift": "Check carrier gas purity or thermal instability in oven.",
            "Noise": "Baseline noise could indicate detector instability or dirty gases.",
            "Unknown": "The model could not confidently classify this trace. Review manually."
        }

        st.markdown(f"{feedback_map.get(label, 'No feedback available.')}")

    except Exception as e:
        st.error(f"Model Error: {str(e)}")