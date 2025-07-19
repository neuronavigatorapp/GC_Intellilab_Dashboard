
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.onboarding_model import InstrumentOnboarding, Base
from datetime import datetime

# DB setup
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

# Page config
st.set_page_config(page_title="🧾 Calibration Overview", layout="centered")
st.markdown("<h1 style='text-align: center;'>🧾 Calibration Summary</h1>", unsafe_allow_html=True)

records = session.query(InstrumentOnboarding).filter(InstrumentOnboarding.status == "complete").all()

if not records:
    st.info("No calibration records found.")
else:
    table = []
    for r in records:
        try:
            cal_date = datetime.strptime(r.last_cal, "%Y-%m-%d").date()
            days_since = (datetime.today().date() - cal_date).days
        except:
            cal_date = "Unknown"
            days_since = "?"

        table.append({
            "Serial": r.serial,
            "Model": f"{r.brand} {r.model}",
            "Method": r.method,
            "Last Cal": str(cal_date),
            "Days Ago": days_since
        })

    import pandas as pd
    df = pd.DataFrame(table).sort_values("Days Ago", ascending=False)
    st.dataframe(df, use_container_width=True)

session.close()
