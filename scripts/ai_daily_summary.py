import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from ai_modules.diagnostic_llm import ask_diagnostic

# 1️⃣ Database Setup
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})

# 2️⃣ Load Data Tables
instruments = pd.read_sql("SELECT * FROM gc_instruments", con=engine)
calibrations = pd.read_sql("SELECT * FROM gc_calibrations", con=engine)
faults = pd.read_sql("SELECT * FROM gc_troubleshooting", con=engine)
inventory = pd.read_sql("SELECT * FROM gc_consumables", con=engine)

# 3️⃣ Compile Text Summary Context
context = f"""📊 IntelliLab GC System Summary – {datetime.now().strftime('%Y-%m-%d')}

🧪 Instruments: {len(instruments)}
🧬 Calibrations Logged: {len(calibrations)}
⚠️ Open Faults: {faults[faults['status'] == 'Open'].shape[0]}
📦 Low Inventory Items: {inventory[inventory['quantity'] <= inventory['reorder_point']].shape[0]}

🔬 Recent Calibration Failures:
{calibrations[calibrations['status'] == 'Fail'][['instrument_serial','compound','response_factor']].head().to_string(index=False)}

🛠 Recent Open Faults:
{faults[faults['status'] == 'Open'][['instrument_serial','fault_type','date']].head().to_string(index=False)}
"""

# 4️⃣ Ask the Local LLM
response = ask_diagnostic("What should we investigate or act on today?", context)

# 5️⃣ Save to File
report_path = "ai_daily_summary.txt"
with open(report_path, "w") as f:
    f.write("=== GC SYSTEM SUMMARY ===\n")
    f.write(context + "\n\n")
    f.write("=== AI RECOMMENDATIONS ===\n")
    f.write(response)

print("✅ AI summary saved to ai_daily_summary.txt")

# 6️⃣ (Optional) Send Email
SEND_EMAIL = False
if SEND_EMAIL:
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg.set_content(response)
    msg["Subject"] = "📊 IntelliLab GC Daily Summary"
    msg["From"] = "you@example.com"
    msg["To"] = "lab.supervisor@example.com"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("you@example.com", "your_app_password")
            server.send_message(msg)
            print("📧 Email sent.")
    except Exception as e:
        print(f"❌ Email failed: {e}")

# 7️⃣ (Optional) Send Slack Message
SEND_SLACK = False
if SEND_SLACK:
    import requests
    SLACK_WEBHOOK = "https://hooks.slack.com/services/XXX/XXX/XXX"
    try:
        requests.post(SLACK_WEBHOOK, json={"text": f"📊 *GC IntelliLab Daily Summary*\n\n{response}"})
        print("✅ Slack message sent.")
    except Exception as e:
        print(f"❌ Slack failed: {e}")
