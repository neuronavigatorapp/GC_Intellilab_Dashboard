
import streamlit as st
import os
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Fix for relative import of models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.onboarding_model import InstrumentOnboarding, Base

# DB setup
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# Page config
st.set_page_config(page_title="🧠 AI Home Mode", layout="centered", initial_sidebar_state="collapsed")

# CSS
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    label, textarea, input, select { font-size: 0.95rem !important; }
    @media screen and (max-width: 600px) {
        h1, h2, h3 { font-size: 1.5rem !important; }
        button[kind="primary"] { font-size: 1rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🧠 AI Home Mode</h1>", unsafe_allow_html=True)

# Load or create onboarding session
latest = session.query(InstrumentOnboarding).filter(InstrumentOnboarding.status == "incomplete").order_by(InstrumentOnboarding.created_at.desc()).first()

if latest:
    st.info(f"🔄 Resuming onboarding for instrument: **{latest.serial}**")
else:
    latest = InstrumentOnboarding(serial="", status="incomplete")
    session.add(latest)
    session.commit()

# Step 1: Instrument Info
st.markdown("### 1️⃣ Instrument Info")
with st.form("instrument_info"):
    latest.serial = st.text_input("Serial Number", value=latest.serial)
    latest.brand = st.selectbox("Brand", ["Agilent", "PerkinElmer", "Shimadzu", "Other"], index=0 if not latest.brand else ["Agilent", "PerkinElmer", "Shimadzu", "Other"].index(latest.brand))
    latest.model = st.text_input("Model", value=latest.model)
    detector_list = ["FID", "TCD", "SCD", "ECD", "FPD", "MS"]
    selected_detectors = st.multiselect("Detector(s) Used", detector_list, default=latest.detectors.split(",") if latest.detectors else [])
    latest.column = st.text_input("Column Type / Phase", value=latest.column)
    if st.form_submit_button("Next"):
        latest.detectors = ",".join(selected_detectors)
        session.commit()
        st.experimental_rerun()

# Step 2: Method Info
if latest.serial and latest.brand:
    st.markdown("### 2️⃣ Method & Sample Info")
    with st.form("method_info"):
        latest.method = st.text_input("GC Method (ASTM/GPA/Other)", value=latest.method)
        latest.sample_types = st.text_area("Sample Types Run", value=latest.sample_types)
        latest.last_cal = st.text_input("Last Calibration Date", value=latest.last_cal or str(datetime.today().date()))
        latest.frequency = st.selectbox("Calibration Frequency", ["Daily", "Weekly", "Monthly", "Other"], index=0 if not latest.frequency else ["Daily", "Weekly", "Monthly", "Other"].index(latest.frequency))
        if st.form_submit_button("Next"):
            session.commit()
            st.experimental_rerun()

# Step 3: Upload Image
if latest.method:
    st.markdown("### 3️⃣ Upload Screenshot (Optional)")
    with st.form("upload_img"):
        img = st.file_uploader("Upload a screenshot or instrument photo (optional)", type=["jpg", "jpeg", "png"])
        if st.form_submit_button("Finish & Save"):
            if img:
                save_dir = "./data/shared_files"
                os.makedirs(save_dir, exist_ok=True)
                path = os.path.join(save_dir, f"{latest.serial}_chromatogram.png")
                with open(path, "wb") as f:
                    f.write(img.getbuffer())
                latest.image_path = path
            latest.status = "complete"
            session.commit()
            st.success("✅ Instrument registered.")
            st.markdown("#### Summary:")
            st.markdown(f"**Serial:** {latest.serial}")
            st.markdown(f"**Brand/Model:** {latest.brand} {latest.model}")
            st.markdown(f"**Detector(s):** {latest.detectors}")
            st.markdown(f"**Column:** {latest.column}")
            st.markdown(f"**Method:** {latest.method}")
            st.markdown(f"**Samples:** {latest.sample_types}")
            st.markdown(f"**Last Cal:** {latest.last_cal} ({latest.frequency})")
            if latest.image_path:
                st.image(latest.image_path, caption="Uploaded Screenshot", use_column_width=True)

session.close()
