# utils/reminder_engine.py

import json
import os
from datetime import datetime, timedelta

REMINDER_FILE = "data/reminders.json"
DEFAULT_INTERVALS = {
    "calibration": 7,
    "inventory_check": 14,
    "maintenance_log": 30,
    "review_qc_plot": 5
}

os.makedirs("data", exist_ok=True)


def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    else:
        return {}


def save_reminders(data):
    with open(REMINDER_FILE, "w") as f:
        json.dump(data, f, indent=2)


def check_due():
    reminders = load_reminders()
    due_now = []
    today = datetime.today().date()

    for key, days in DEFAULT_INTERVALS.items():
        last = reminders.get(key, {}).get("last_done")
        if not last:
            due_now.append(key)
        else:
            last_date = datetime.strptime(last, "%Y-%m-%d").date()
            if (today - last_date).days >= days:
                due_now.append(key)

    return due_now


def mark_done(task):
    reminders = load_reminders()
    reminders[task] = {"last_done": datetime.today().strftime("%Y-%m-%d")}
    save_reminders(reminders)