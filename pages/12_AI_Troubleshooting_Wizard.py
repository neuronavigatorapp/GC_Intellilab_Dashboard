import streamlit as st
from ai_modules.diagnostic_llm import ask_diagnostic, build_gc_context

st.set_page_config(page_title="🧠 GC AI Wizard", layout="centered")

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

st.title("🧠 Guided GC Troubleshooting Wizard")

with st.form("wizard"):
    st.subheader("Step 1: Select Instrument")
    serial = st.text_input("Instrument Serial Number")

    st.subheader("Step 2: Detector Type")
    detector = st.selectbox("Which detector is involved?", ["FID", "TCD", "SCD", "Methanizer", "Other"])

    st.subheader("Step 3: What are you seeing?")
    symptom = st.selectbox("Select the symptom:", [
        "Tailing", "Fronting", "No Peaks", "Low Signal", "Baseline Drift", "Ghost Peaks",
        "Negative Peaks", "Backflush Error", "Retention Time Drift", "Other"
    ])

    st.subheader("Step 4: Method + Notes")
    method = st.text_input("GC Method (e.g. D6730, D5504)", placeholder="Optional")
    notes = st.text_area("Any other info? (e.g. compounds affected, last maintenance, etc.)", height=100)

    submitted = st.form_submit_button("Diagnose Issue")

# Process
if submitted:
    st.subheader("🔍 Building prompt...")

    auto_context = build_gc_context(serial) if serial else ""
    prompt = f"""Instrument Serial: {serial or 'N/A'}
Detector: {detector}
Method: {method or 'N/A'}
Observed Symptom: {symptom}

Additional Notes:
{notes}

Recent History:
{auto_context}
    """

    st.code(prompt, language="markdown")

    st.subheader("🧠 AI Suggestion")
    with st.spinner("Asking local assistant..."):
        result = ask_diagnostic(f"What is the most likely root cause and next step?", prompt)

    st.markdown(f"```markdown\n{result}\n```")