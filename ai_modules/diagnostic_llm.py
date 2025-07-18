import requests
import pandas as pd
from sqlalchemy import create_engine

# 1️⃣ Ollama Settings
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"

# 2️⃣ Ask the AI
def ask_diagnostic(question: str, context: str = "", model: str = DEFAULT_MODEL):
    system_prompt = (
        "You are a GC diagnostic assistant trained on ASTM, GPA, and EPA GC methods. "
        "You help chemists troubleshoot chromatographic issues, analyze QC trends, and recommend actions. "
        "Respond clearly and technically."
    )

    full_prompt = f"<|system|>{system_prompt}\n<|user|>{context}\n\nQ: {question}"

    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "⚠️ No response received.")
    except Exception as e:
        return f"❌ Error contacting Ollama: {e}"

# 3️⃣ Build Auto Context from DB
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})

def build_gc_context(serial: str):
    context_parts = []

    try:
        # Instrument Info
        inst = pd.read_sql(f"""
            SELECT model, channels, detectors, methods_supported 
            FROM gc_instruments 
            WHERE serial_number = '{serial}'
        """, engine)
        if not inst.empty:
            row = inst.iloc[0]
            context_parts.append(f"Instrument: {row['model']} | Channels: {row['channels']} | Detectors: {row['detectors']} | Methods: {row['methods_supported']}")

        # Recent Calibrations
        cal = pd.read_sql(f"""
            SELECT compound, response_factor, calibration_date, status 
            FROM gc_calibrations 
            WHERE instrument_serial = '{serial}' 
            ORDER BY calibration_date DESC LIMIT 5
        """, engine)
        if not cal.empty:
            context_parts.append("Recent Calibration Events:")
            for _, row in cal.iterrows():
                context_parts.append(f" - {row['compound']}: RF={row['response_factor']} ({row['status']}) on {row['calibration_date'][:10]}")

        # Recent Troubleshooting Logs
        faults = pd.read_sql(f"""
            SELECT method, detector, fault_type, date, status 
            FROM gc_troubleshooting 
            WHERE instrument_serial = '{serial}' 
            ORDER BY date DESC LIMIT 5
        """, engine)
        if not faults.empty:
            context_parts.append("Recent Troubleshooting Events:")
            for _, row in faults.iterrows():
                context_parts.append(f" - {row['date'][:10]} | {row['detector']} | {row['fault_type']} ({row['status']})")
    except:
        pass

    return "\n".join(context_parts) if context_parts else "No recent system data available."
