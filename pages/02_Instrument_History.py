
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.onboarding_model import InstrumentOnboarding, Base

# DB setup
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

# Page setup
st.set_page_config(page_title="📋 Instrument History", layout="centered")
st.markdown("<h1 style='text-align: center;'>📋 Instrument History</h1>", unsafe_allow_html=True)

records = session.query(InstrumentOnboarding).order_by(InstrumentOnboarding.created_at.desc()).all()

if not records:
    st.info("No instruments onboarded yet.")
else:
    status_filter = st.selectbox("Filter by status", ["All", "complete", "incomplete"])
    if status_filter != "All":
        records = [r for r in records if r.status == status_filter]

    for r in records:
        st.markdown("---")
        st.markdown(f"**Serial:** {r.serial}")
        st.markdown(f"**Model:** {r.brand} {r.model}")
        st.markdown(f"**Method:** {r.method}")
        st.markdown(f"**Status:** `{r.status}`")
        st.markdown(f"**Last Cal:** {r.last_cal or 'N/A'} ({r.frequency})")
        if r.image_path and os.path.exists(r.image_path):
            st.image(r.image_path, caption="Chromatogram", use_column_width=True)

session.close()
