import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Interactive Troubleshooting", layout="centered")

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

st.title("🚨 GC Advanced Interactive Troubleshooting")

# Data directory for historical troubleshooting logs
DATA_DIR = "../data/troubleshooting"
os.makedirs(DATA_DIR, exist_ok=True)
troubleshoot_csv = os.path.join(DATA_DIR, "troubleshooting_records.csv")

# Load existing troubleshooting records or create empty dataframe
if os.path.exists(troubleshoot_csv):
    troubleshoot_df = pd.read_csv(troubleshoot_csv)
else:
    troubleshoot_df = pd.DataFrame(columns=[
        "Instrument_Name", "Issue_Type", "Detailed_Description",
        "Date_Logged", "AI_Recommended_Steps", "Technician", "Resolved"
    ])

# Sidebar: Log New Troubleshooting Issue
st.sidebar.header("➕ Log New Troubleshooting Issue")

with st.sidebar.form("troubleshoot_form"):
    instrument_name = st.text_input("Instrument Name")
    issue_type = st.selectbox("Common Issue", [
        "Column Installation Error", "Phase Depletion", "Carrier Gas EPC Issue",
        "FID Detector Issue", "TCD Detector Issue", "SCD (Single Plasma) Issue",
        "SCD (Dual Plasma) Issue", "Methanizer Issue", "VICI Valve Leak",
        "Backflush Timing Issue", "Injector/Syringe Issue", "Baseline Drift",
        "Contaminant Carryover", "Other"
    ])
    detailed_description = st.text_area("Detailed Description of Issue")
    technician = st.text_input("Reported by (Technician)")
    date_logged = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    submitted = st.form_submit_button("Run AI Troubleshooting")

    if submitted:
        # Call AI Troubleshooting Backend
        payload = {
            "issue_description": f"{issue_type}: {detailed_description}",
            "recent_actions": ""
        }
        response = requests.post("http://localhost:8000/ai-troubleshoot-advanced/", json=payload)
        
        if response.ok:
            ai_steps = response.json()["troubleshooting_steps"]
            st.sidebar.success("AI troubleshooting completed successfully!")
        else:
            ai_steps = "AI troubleshooting service unavailable."
            st.sidebar.error("AI troubleshooting failed.")

        new_record = {
            "Instrument_Name": instrument_name,
            "Issue_Type": issue_type,
            "Detailed_Description": detailed_description,
            "Date_Logged": date_logged,
            "AI_Recommended_Steps": ai_steps,
            "Technician": technician,
            "Resolved": "No"
        }
        troubleshoot_df = troubleshoot_df.append(new_record, ignore_index=True)
        troubleshoot_df.to_csv(troubleshoot_csv, index=False)

# Main Page: Troubleshooting History and AI Recommendations
st.subheader("📋 Troubleshooting History")

if not troubleshoot_df.empty:
    st.dataframe(troubleshoot_df, use_container_width=True)

    # Filter troubleshooting records
    with st.expander("🔍 Filter Troubleshooting Records"):
        filter_instrument = st.selectbox("Filter by Instrument", ["All"] + troubleshoot_df["Instrument_Name"].unique().tolist())
        filter_issue = st.selectbox("Filter by Issue Type", ["All"] + troubleshoot_df["Issue_Type"].unique().tolist())
        resolution_status = st.selectbox("Resolution Status", ["All", "Yes", "No"])

        filtered_df = troubleshoot_df.copy()
        if filter_instrument != "All":
            filtered_df = filtered_df[filtered_df["Instrument_Name"] == filter_instrument]
        if filter_issue != "All":
            filtered_df = filtered_df[filtered_df["Issue_Type"] == filter_issue]
        if resolution_status != "All":
            filtered_df = filtered_df[filtered_df["Resolved"] == resolution_status]

        st.dataframe(filtered_df, use_container_width=True)

    # Mark issue as resolved
    with st.expander("✅ Mark Issue as Resolved"):
        unresolved_issues = troubleshoot_df[troubleshoot_df["Resolved"] == "No"]["Detailed_Description"].tolist()
        if unresolved_issues:
            issue_to_resolve = st.selectbox("Select Issue to Mark Resolved", unresolved_issues)
            if st.button("Mark as Resolved"):
                troubleshoot_df.loc[troubleshoot_df["Detailed_Description"] == issue_to_resolve, "Resolved"] = "Yes"
                troubleshoot_df.to_csv(troubleshoot_csv, index=False)
                st.success("Issue marked as resolved. Refresh to update.")
        else:
            st.success("No unresolved issues currently.")
else:
    st.info("No troubleshooting issues logged yet. Use the sidebar to log an issue.")