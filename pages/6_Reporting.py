import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# DB setup
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})

st.set_page_config(page_title="📄 GC Reports", layout="wide")
st.title("📄 Reporting & Documentation")

# Report type
report_type = st.selectbox("Select Report Type", [
    "Instrument Registry",
    "Inventory Summary",
    "Calibration Summary",
    "Troubleshooting Log"
])

# Load relevant table
if report_type == "Instrument Registry":
    df = pd.read_sql("SELECT * FROM gc_instruments", con=engine)
elif report_type == "Inventory Summary":
    df = pd.read_sql("SELECT * FROM gc_consumables", con=engine)
elif report_type == "Calibration Summary":
    df = pd.read_sql("SELECT * FROM gc_calibrations", con=engine)
elif report_type == "Troubleshooting Log":
    df = pd.read_sql("SELECT * FROM gc_troubleshooting", con=engine)
else:
    df = pd.DataFrame()

# Display + Export
if df.empty:
    st.info("No records found.")
else:
    st.dataframe(df, use_container_width=True)
    st.download_button(
        label=f"📥 Download {report_type} (CSV)",
        data=df.to_csv(index=False),
        file_name=f"{report_type.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )
