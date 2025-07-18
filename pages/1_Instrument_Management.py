import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Instrument Management", layout="wide")
st.title("🔧 GC Instrument Management & Predictive Health")

# Data persistence directory
DATA_DIR = "../data/instrument_profiles"
os.makedirs(DATA_DIR, exist_ok=True)
profiles_csv = os.path.join(DATA_DIR, "instrument_profiles.csv")

# Load existing profiles
if os.path.exists(profiles_csv):
    profiles_df = pd.read_csv(profiles_csv)
else:
    profiles_df = pd.DataFrame(columns=[
        "Instrument_Name", "Serial_Number", "GC_Model", "Channel_Mode",
        "Column_Type", "Carrier_Gas", "Detector_Type", "Method",
        "Created_On", "Avg_Daily_Usage_Hours", "Last_Maintenance_Date"
    ])

# Add New Instrument Profile
st.sidebar.header("➕ Add New Instrument Profile")
with st.sidebar.form("new_profile_form"):
    instrument_name = st.text_input("Instrument Name")
    serial_number = st.text_input("Serial Number")
    gc_model = st.selectbox("GC Model", ["Agilent 6890", "Agilent 7890", "Agilent 8890"])
    channel_mode = st.selectbox("Channel Mode", ["Single", "Dual"])
    column_type = st.selectbox("Column Type", ["DB-1", "DB-5", "MAPD", "LowOx", "Packed"])
    carrier_gas = st.selectbox("Carrier Gas", ["Helium (He)", "Nitrogen (N₂)", "Hydrogen (H₂)"])
    detector_type = st.multiselect("Detector(s)", ["FID", "TCD", "SCD (Single Plasma)", "SCD (Dual Plasma)", "Methanizer"])
    method = st.text_input("Method Reference (e.g., ASTM D6730)")
    avg_daily_usage = st.number_input("Average Daily Usage (Hours)", min_value=0, step=1)
    last_maintenance_date = st.date_input("Last Maintenance Date", datetime.today())
    submitted = st.form_submit_button("Save Profile")

    if submitted:
        new_profile = {
            "Instrument_Name": instrument_name,
            "Serial_Number": serial_number,
            "GC_Model": gc_model,
            "Channel_Mode": channel_mode,
            "Column_Type": column_type,
            "Carrier_Gas": carrier_gas,
            "Detector_Type": "; ".join(detector_type),
            "Method": method,
            "Created_On": datetime.now().strftime("%Y-%m-%d"),
            "Avg_Daily_Usage_Hours": avg_daily_usage,
            "Last_Maintenance_Date": last_maintenance_date.strftime("%Y-%m-%d")
        }
        profiles_df = profiles_df.append(new_profile, ignore_index=True)
        profiles_df.to_csv(profiles_csv, index=False)
        st.sidebar.success(f"Instrument '{instrument_name}' profile saved!")

# Instrument Predictive Health Analytics
st.subheader("📈 Predictive Instrument Health Analysis")

if not profiles_df.empty:
    profiles_df["Days_Since_Maintenance"] = (datetime.now() - pd.to_datetime(profiles_df["Last_Maintenance_Date"])).dt.days
    profiles_df["Projected_Days_to_Next_Maintenance"] = 90 - profiles_df["Days_Since_Maintenance"]

    fig = px.bar(profiles_df, x="Instrument_Name", y="Projected_Days_to_Next_Maintenance", color="GC_Model",
                 labels={"Projected_Days_to_Next_Maintenance": "Days Until Next PM"},
                 title="Projected Days Until Next Preventive Maintenance")
    st.plotly_chart(fig, use_container_width=True)

    at_risk = profiles_df[profiles_df["Projected_Days_to_Next_Maintenance"] <= 14]
    if not at_risk.empty:
        st.warning("⚠️ Instruments requiring maintenance within 2 weeks:")
        st.dataframe(at_risk[["Instrument_Name", "Days_Since_Maintenance", "Projected_Days_to_Next_Maintenance"]])
    else:
        st.success("All instruments have adequate maintenance schedules.")
else:
    st.info("No instrument profiles found. Add profiles from the sidebar.")
