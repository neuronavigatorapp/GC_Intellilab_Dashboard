import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.db_models_calibration import GCCalibration, Base  # ✅ Fixed import
from datetime import datetime

# 1️⃣ DB Setup
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

# 2️⃣ Page Setup
st.set_page_config(page_title="🎯 QC & Calibration", layout="centered")

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

st.title("🎯 GC Calibration & QC Logging")

# 3️⃣ Input Form
with st.expander("➕ Add Calibration Event"):
    with st.form("calibration_form"):
        serial = st.text_input("Instrument Serial")
        method = st.selectbox("Method", sorted([
            "D1945", "D2163", "D6730", "D5504", "D7423", "D5134", "D7862", "Other"
        ]))
        compound = st.text_input("Compound")
        rf = st.number_input("Response Factor", min_value=0.0)
        status = st.selectbox("Status", ["Pass", "Warning", "Fail"])
        analyst = st.text_input("Analyst")
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Log Calibration")

    if submit:
        new_cal = GCCalibration(
            instrument_serial=serial,
            method=method,
            compound=compound,
            response_factor=rf,
            status=status,
            analyst=analyst,
            notes=notes,
            calibration_date=datetime.utcnow()
        )
        session.add(new_cal)
        session.commit()
        st.success(f"{compound} calibration logged for {serial}.")

# 4️⃣ View + Filter Data
st.subheader("📊 Calibration History")

df = pd.read_sql("SELECT * FROM gc_calibrations", con=engine)

if df.empty:
    st.info("No calibration records yet.")
else:
    serials = df["instrument_serial"].unique().tolist()
    serial_filter = st.selectbox("Filter by Instrument Serial", ["All"] + serials)
    if serial_filter != "All":
        df = df[df["instrument_serial"] == serial_filter]

    st.dataframe(df.sort_values("calibration_date", ascending=False), use_container_width=True)

    # 📈 Optional Drift Plot
    st.subheader("📈 Response Factor Trend")
    comp_filter = st.selectbox("Select Compound to Plot", df["compound"].unique())
    trend_df = df[df["compound"] == comp_filter]
    fig = px.line(trend_df, x="calibration_date", y="response_factor", color="status", markers=True)
    fig.update_layout(title=f"Response Factor Trend: {comp_filter}", xaxis_title="Date", yaxis_title="RF")
    st.plotly_chart(fig, use_container_width=True)

session.close()