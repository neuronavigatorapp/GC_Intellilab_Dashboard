import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.db_models_instruments import GCInstrument, Base

# 1️⃣ Connect to DB
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

# 2️⃣ Page Setup (centered for mobile)
st.set_page_config(page_title="🧪 GC Instruments", layout="centered")
st.title("🧪 Instrument Management")

# 3️⃣ Instrument Form
with st.form("add_gc_form"):
    st.markdown("### ➕ Add New GC Instrument")
    name = st.text_input("Instrument Name", placeholder="GC-01 - Reformate Analyzer")
    serial_number = st.text_input("Serial Number", placeholder="US6890A12345")
    model = st.selectbox("Model", ["Agilent 6890", "Agilent 7890", "Agilent 8890", "Other"])
    channels = st.radio("Channel Count", ["Single", "Dual"], horizontal=True)
    detectors = st.multiselect("Detector Types", ["FID", "TCD", "SCD", "ECD", "Methanizer"])
    methods = st.multiselect("Supported ASTM/GPA Methods", sorted([
        "D1945", "D1946", "D2163", "D2593", "D2712", "D4815", "D5134", "D5441", "D5501", "D5504",
        "D5580", "D5599", "D5623", "D6550", "D6729", "D6730", "D7011", "D7423", "D7756", "D7833",
        "D7862", "D7994", "D8071"
    ]))
    location = st.text_input("Lab Location", placeholder="e.g. Deer Park Lab")
    notes = st.text_area("Notes or Special Configuration", height=80)

    submit = st.form_submit_button("✅ Add Instrument")

# 4️⃣ Save Entry
if submit:
    new_gc = GCInstrument(
        name=name,
        serial_number=serial_number,
        model=model,
        channels=channels,
        detectors=",".join(detectors),
        methods_supported=",".join(methods),
        location=location,
        notes=notes
    )
    session.add(new_gc)
    session.commit()
    st.success(f"Instrument '{name}' was added successfully!")

# 5️⃣ Instrument Table
st.markdown("### 📋 Registered Instruments")
gcs = session.query(GCInstrument).all()

if not gcs:
    st.info("No instruments registered yet.")
else:
    df = pd.DataFrame([{
        "Name": gc.name,
        "Serial #": gc.serial_number,
        "Model": gc.model,
        "Channels": gc.channels,
        "Detectors": gc.detectors,
        "Methods": gc.methods_supported,
        "Location": gc.location,
        "Notes": gc.notes
    } for gc in gcs])

    st.dataframe(df, use_container_width=True)

session.close()
