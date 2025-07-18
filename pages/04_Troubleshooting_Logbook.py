import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models_troubleshooting import GCTroubleshooting

# 1️⃣ DB Setup
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

# 2️⃣ Page Setup
st.set_page_config(page_title="🔍 GC Troubleshooting Logbook", layout="wide")
st.title("🔍 Troubleshooting Logbook")

# 3️⃣ Add New Issue
with st.expander("➕ Log New GC Issue"):
    with st.form("trouble_form"):
        serial = st.text_input("Instrument Serial Number")
        method = st.selectbox("Method", sorted([
            "D1945", "D1946", "D2163", "D2593", "D2712", "D4815", "D5134", "D5504", "D6730", "D7423", "Other"
        ]))
        detector = st.selectbox("Detector", ["FID", "TCD", "SCD", "ECD", "Methanizer"])
        fault = st.text_input("Fault Type (e.g. Ghost Peak, Signal Drop, Fronting)")
        description = st.text_area("Issue Description")
        resolution = st.text_area("Resolution (optional)")
        operator = st.text_input("Operator")
        status = st.selectbox("Status", ["Open", "Closed", "Escalated"])
        submit = st.form_submit_button("Log Issue")

    if submit:
        issue = GCTroubleshooting(
            instrument_serial=serial,
            method=method,
            detector=detector,
            fault_type=fault,
            description=description,
            resolution=resolution,
            operator=operator,
            status=status,
            date=datetime.utcnow()
        )
        session.add(issue)
        session.commit()
        st.success("Issue logged.")

# 4️⃣ View Log History
st.subheader("📋 Troubleshooting History")

logs = session.query(GCTroubleshooting).order_by(GCTroubleshooting.date.desc()).all()

if not logs:
    st.info("No troubleshooting records yet.")
else:
    data = [{
        "Date": i.date.strftime("%Y-%m-%d"),
        "Instrument": i.instrument_serial,
        "Method": i.method,
        "Detector": i.detector,
        "Fault": i.fault_type,
        "Status": i.status,
        "Operator": i.operator,
        "Description": i.description,
        "Resolution": i.resolution
    } for i in logs]

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "📥 Export Logbook as CSV",
        df.to_csv(index=False),
        "troubleshooting_logbook.csv",
        "text/csv"
    )

session.close()
