import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Collaborative GC Dashboard", layout="wide")
st.title("📊 Real-time Collaborative GC Lab Dashboard")

# Data directories for collaborative data
DATA_DIR = "../data/collaboration"
os.makedirs(DATA_DIR, exist_ok=True)
messages_csv = os.path.join(DATA_DIR, "team_messages.csv")

# Load or create team message data
if os.path.exists(messages_csv):
    messages_df = pd.read_csv(messages_csv)
else:
    messages_df = pd.DataFrame(columns=["Timestamp", "Username", "Message"])

# User login (simplified for demo; replace with robust authentication later)
st.sidebar.header("👤 User Login")
username = st.sidebar.text_input("Enter your Username")

if username:
    st.sidebar.success(f"Logged in as: {username}")

    # Post new team message
    st.sidebar.header("💬 Post Team Message")
    with st.sidebar.form("message_form"):
        message = st.text_area("Message")
        post_message = st.form_submit_button("Post Message")

        if post_message and message:
            new_message = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Username": username,
                "Message": message
            }
            messages_df = messages_df.append(new_message, ignore_index=True)
            messages_df.to_csv(messages_csv, index=False)
            st.sidebar.success("Message posted successfully!")
        elif post_message and not message:
            st.sidebar.error("Message cannot be empty!")

    # Main Page: Team Message Board
    st.subheader("📢 Team Message Board (Real-time)")
    if not messages_df.empty:
        recent_messages = messages_df.sort_values("Timestamp", ascending=False).head(20)
        for idx, row in recent_messages.iterrows():
            st.markdown(f"**{row['Username']}** [{row['Timestamp']}]  \n> {row['Message']}")
    else:
        st.info("No messages yet. Post your first team message!")

    # Real-time Instrument & Maintenance Status Visualization
    st.subheader("📈 Instrument & Maintenance Status Overview")
    maintenance_csv = "../data/maintenance/maintenance_records.csv"
    if os.path.exists(maintenance_csv):
        maintenance_df = pd.read_csv(maintenance_csv)
        maintenance_df["Days_Until_PM"] = (pd.to_datetime(maintenance_df["Next_PM_Due"]) - datetime.now()).dt.days

        fig = px.bar(maintenance_df, x="Instrument_Name", y="Days_Until_PM", color="Maintenance_Type",
                     labels={"Days_Until_PM": "Days Until Next PM"},
                     title="Real-time Instrument Maintenance Status")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Maintenance data not found. Please log maintenance activities.")

    # Collaborative Data Sharing Placeholder
    st.subheader("🔒 Secure Data Sharing (Coming Soon)")
    st.info("Upcoming enhancement: Secure, role-based data sharing for sensitive documents and results.")

else:
    st.sidebar.warning("Please enter your username to access collaborative features.")
