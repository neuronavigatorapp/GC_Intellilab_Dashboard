import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from ai_modules.diagnostic_llm import ask_diagnostic

st.set_page_config(page_title="📊 Daily GC Summary", layout="wide")
st.title("📊 GC System Summary & AI Alert Review")

# 1️⃣ Load DB
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})

# 2️⃣ Fetch key tables
instruments = pd.read_sql("SELECT * FROM gc_instruments", con=engine)
calibrations = pd.read_sql("SELECT * FROM gc_calibrations", con=engine)
faults = pd.read_sql("SELECT * FROM gc_troubleshooting", con=engine)
inventory = pd.read_sql("SELECT * FROM gc_consumables", con=engine)

# 3️⃣ Summarize content
st.subheader("📋 System Overview")

st.metric("Instruments", len(instruments))
st.metric("Total Calibrations", len(calibrations))
st.metric("Open Faults", faults[faults["status"] == "Open"].shape[0])
st.metric("Low Inventory Items", inventory[inventory["quantity"] <= inventory["reorder_point"]].shape[0])

# 4️⃣ Optional AI Analysis
st.subheader("🧠 AI Summary & Alerts")

compiled_context = f"""Today's system state summary:

Instruments: {len(instruments)}
Total calibrations: {len(calibrations)}
Open troubleshooting logs: {faults[faults['status'] == 'Open'].shape[0]}
Low inventory items: {inventory[inventory['quantity'] <= inventory['reorder_point']].shape[0]}

Recent calibration failures:
{calibrations[calibrations['status'] == 'Fail'][['instrument_serial','compound','response_factor']].head().to_string(index=False)}

Unresolved troubleshooting events:
{faults[faults['status'] == 'Open'][['instrument_serial','fault_type','date']].head().to_string(index=False)}
"""

st.code(compiled_context)

ask = st.button("🧠 Analyze With AI")

if ask:
    with st.spinner("Reviewing system health..."):
        summary = ask_diagnostic("What should I look into or fix today?", compiled_context)
    st.subheader("📋 AI Action Summary")
    st.markdown(f"```markdown\n{summary}\n```")
