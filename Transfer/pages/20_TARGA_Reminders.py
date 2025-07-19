# pages/20_TARGA_Reminders.py

import streamlit as st
from utils.reminder_engine import check_due, mark_done, load_reminders
from datetime import datetime

st.set_page_config(page_title="TARGA Reminders", layout="centered")
st.title("🔔 TARGA Task Reminders")

st.markdown("""
Stay on track with critical lab activities. These reminders are based on suggested intervals and reset when completed.
""")

# 1️⃣ View Due Tasks
due_tasks = check_due()

if due_tasks:
    st.subheader("🔶 Due Now")
    for task in due_tasks:
        if st.button(f"Mark '{task.replace('_', ' ').title()}' as Done"):
            mark_done(task)
            st.success(f"✅ Marked '{task}' complete.")
else:
    st.success("✅ No overdue tasks.")

# 2️⃣ View History
st.markdown("---")
st.subheader("🗓 Last Completed")
history = load_reminders()
if not history:
    st.info("No task history available yet.")
else:
    for task, entry in history.items():
        st.text(f"{task.replace('_', ' ').title()}: {entry['last_done']}")
