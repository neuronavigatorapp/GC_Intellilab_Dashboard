import streamlit as st
import pandas as pd
from sqlalchemy.orm import sessionmaker
from utils.db_models import GCDiagnostic, engine

st.set_page_config(page_title="📜 GC Diagnostic History", layout="centered")

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

st.title("📜 GC AI Diagnostic History")

# Setup DB session
Session = sessionmaker(bind=engine)
session = Session()

# Load diagnostics
diagnostics = session.query(GCDiagnostic).order_by(GCDiagnostic.timestamp.desc()).all()
session.close()

if not diagnostics:
    st.info("No diagnostics saved yet. Try running a simulation first.")
else:
    # Prepare data for table
    df = pd.DataFrame([{
        "Timestamp": d.timestamp.strftime("%Y-%m-%d %H:%M"),
        "Inlet Temp": d.inlet_temp,
        "Oven": f"{d.oven_start} → {d.oven_final} @ {d.ramp_rate}°C/min, hold {d.hold_time}min",
        "Flow (mL/min)": d.flow_rate,
        "Column": d.column_type,
        "Detector": d.detector,
        "User Question": d.user_question,
        "AI Response": d.ai_response
    } for d in diagnostics])

    st.dataframe(df, use_container_width=True)

    with st.expander("📋 View Full Entries"):
        for d in diagnostics:
            st.markdown(f"### 🕒 {d.timestamp.strftime('%Y-%m-%d %H:%M')}")
            st.markdown(f"""
            - **Inlet Temp**: {d.inlet_temp} °C  
            - **Oven**: {d.oven_start} → {d.oven_final} °C @ {d.ramp_rate} °C/min (hold {d.hold_time} min)  
            - **Flow Rate**: {d.flow_rate} mL/min  
            - **Column**: {d.column_type}  
            - **Detector**: {d.detector}  
            - **🧪 Question**: {d.user_question}  
            - **🤖 AI Suggestion**:  
            ```text
            {d.ai_response}
            ```
            """)