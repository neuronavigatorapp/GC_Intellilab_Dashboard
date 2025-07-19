import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models_maintenance import GCMaintenance

# 1️⃣ DB Setup
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

# 2️⃣ Page Setup
st.set_page_config(page_title="🛠 GC Maintenance Logs", layout="wide")
st.title("🛠 Preventive & Corrective Maintenance Log")

# 3️⃣ Entry Form
with st.expander("➕ Log New Maintenance Activity", expanded=False):
    with st.form("maintenance_form"):
        serial = st.text_input("Instrument Serial Number")
        date = st.date_input("Maintenance Date", value=datetime.today())
        service_type = st.selectbox("Service Type", ["PM", "Corrective", "Emergency", "Calibration", "Other"])
        parts = st.text_area("Parts Replaced (if any)")
        technician = st.text_input("Technician")
        notes = st.text_area("Notes or Summary")

        submit = st.form_submit_button("Log Maintenance")

    if submit:
        entry = GCMaintenance(
            instrument_serial=serial,
            date=datetime.combine(date, datetime.min.time()),
            service_type=service_type,
            parts_replaced=parts,
            technician=technician,
            notes=notes
        )
        session.add(entry)
        session.commit()
        st.success("Maintenance entry logged.")

# 4️⃣ View History
st.subheader("📋 Maintenance History")

results = session.query(GCMaintenance).order_by(GCMaintenance.date.desc()).all()

if not results:
    st.info("No maintenance records found.")
else:
    records = []
    for r in results:
        records.append({
            "Date": r.date.strftime("%Y-%m-%d"),
            "Instrument": r.instrument_serial,
            "Type": r.service_type,
            "Technician": r.technician,
            "Parts Replaced": r.parts_replaced,
            "Notes": r.notes
        })
    df = pd.DataFrame(records)
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "📥 Download as CSV",
        data=df.to_csv(index=False),
        file_name="gc_maintenance_log.csv",
        mime="text/csv"
    )

session.close()
