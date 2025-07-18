import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime, timedelta
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Maintenance & AI PM Management", layout="wide")
st.title("🛠 GC Maintenance & AI Predictive Scheduling")

# Data directory
DATA_DIR = "../data/maintenance"
os.makedirs(DATA_DIR, exist_ok=True)
maintenance_csv = os.path.join(DATA_DIR, "maintenance_records.csv")

# Load maintenance records
if os.path.exists(maintenance_csv):
    maintenance_df = pd.read_csv(maintenance_csv)
else:
    maintenance_df = pd.DataFrame(columns=[
        "Instrument_Name", "Maintenance_Type", "Performed_On",
        "Technician", "Details", "Next_PM_Due", "AI_PM_Recommendations"
    ])

# Sidebar: Log Maintenance Activity
st.sidebar.header("➕ Log New Maintenance Activity")
with st.sidebar.form("maintenance_form"):
    instrument_name = st.text_input("Instrument Name")
    maintenance_type = st.selectbox("Maintenance Type", ["Routine", "Preventive", "Corrective", "Calibration"])
    performed_on = st.date_input("Date Performed", datetime.today())
    technician = st.text_input("Technician Name")
    details = st.text_area("Details & Observations")
    next_pm_due = st.date_input("Next PM Due", datetime.today() + timedelta(days=90))
    submitted = st.form_submit_button("Save Activity")

    if submitted:
        payload = {"issue_description": details, "recent_actions": maintenance_type}
        response = requests.post("http://localhost:8000/ai-troubleshoot-advanced/", json=payload)

        ai_recommendations = response.json()["troubleshooting_steps"] if response.ok else "AI unavailable."

        new_record = {
            "Instrument_Name": instrument_name,
            "Maintenance_Type": maintenance_type,
            "Performed_On": performed_on.strftime("%Y-%m-%d"),
            "Technician": technician,
            "Details": details,
            "Next_PM_Due": next_pm_due.strftime("%Y-%m-%d"),
            "AI_PM_Recommendations": ai_recommendations
        }
        maintenance_df = maintenance_df.append(new_record, ignore_index=True)
        maintenance_df.to_csv(maintenance_csv, index=False)
        st.sidebar.success("Maintenance logged with AI recommendations.")

# Predictive Maintenance Schedule Visualization
st.subheader("📅 Predictive PM Scheduling")

if not maintenance_df.empty:
    maintenance_df["Days_Until_PM"] = (pd.to_datetime(maintenance_df["Next_PM_Due"]) - datetime.now()).dt.days
    upcoming_pm = maintenance_df.sort_values("Days_Until_PM")

    fig = px.timeline(upcoming_pm, x_start="Performed_On", x_end="Next_PM_Due", y="Instrument_Name",
                      color="Maintenance_Type", title="Predictive Maintenance Timeline")
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)

    critical_pm = upcoming_pm[upcoming_pm["Days_Until_PM"] <= 14]
    if not critical_pm.empty:
        st.warning("⚠️ Critical upcoming maintenance tasks within 2 weeks:")
        st.dataframe(critical_pm[["Instrument_Name", "Next_PM_Due", "Maintenance_Type", "Days_Until_PM"]])
    else:
        st.success("No critical maintenance tasks pending.")
else:
    st.info("No maintenance records found. Log maintenance activities to begin predictive scheduling.")
