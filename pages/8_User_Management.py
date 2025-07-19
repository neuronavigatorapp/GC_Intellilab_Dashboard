import streamlit as st
import pandas as pd
import os
from datetime import datetime
import hashlib

# Helper functions for password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_pwd, stored_hash):
    return hash_password(input_pwd) == stored_hash

# Page configuration
st.set_page_config(page_title="Secure User & Data Management", layout="centered")

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

st.title("🔐 GC User Management & Secure Authentication")

# Data directories
DATA_DIR = "../data/user_management"
SHARED_DIR = "../data/shared_files"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SHARED_DIR, exist_ok=True)

users_csv = os.path.join(DATA_DIR, "user_accounts.csv")
audit_log_csv = os.path.join(DATA_DIR, "user_audit_trail.csv")

# Initialize or load user data
if os.path.exists(users_csv):
    users_df = pd.read_csv(users_csv)
else:
    users_df = pd.DataFrame(columns=[
        "Username", "Full_Name", "Role", "Password_Hash", "Date_Created", "Last_Login"
    ])

# Sidebar: Admin creates new user accounts
st.sidebar.header("👤 Admin Panel")
admin_password = st.sidebar.text_input("Admin Password", type="password")
ADMIN_PWD_HASH = hash_password("securepassword")  # Replace securely later

if verify_password(admin_password, ADMIN_PWD_HASH):
    st.sidebar.success("Admin access granted.")

    with st.sidebar.form("new_user_form"):
        username = st.text_input("Username")
        full_name = st.text_input("Full Name")
        role = st.selectbox("Role", ["Analyst", "Technician", "Manager", "Administrator"])
        password = st.text_input("Initial Password", type="password")
        submit_user = st.form_submit_button("Create User")

        if submit_user:
            if username not in users_df["Username"].values:
                new_user = {
                    "Username": username,
                    "Full_Name": full_name,
                    "Role": role,
                    "Password_Hash": hash_password(password),
                    "Date_Created": datetime.now().strftime("%Y-%m-%d"),
                    "Last_Login": ""
                }
                users_df = users_df.append(new_user, ignore_index=True)
                users_df.to_csv(users_csv, index=False)
                st.sidebar.success(f"User '{username}' created securely!")
            else:
                st.sidebar.error("Username already exists!")

else:
    st.sidebar.warning("Enter valid admin credentials.")

# User Login
st.sidebar.header("🔑 Secure User Login")
username_input = st.sidebar.text_input("Username")
password_input = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

if login_button:
    if username_input in users_df["Username"].values:
        stored_hash = users_df[users_df["Username"] == username_input]["Password_Hash"].iloc[0]
        if verify_password(password_input, stored_hash):
            user_role = users_df[users_df["Username"] == username_input]["Role"].iloc[0]
            st.sidebar.success(f"Logged in as {username_input} ({user_role})")

            # Update last login
            users_df.loc[users_df["Username"] == username_input, "Last_Login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            users_df.to_csv(users_csv, index=False)

            # Log user activity
            def log_activity(user, action):
                entry = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Username": user,
                    "Action": action
                }
                if os.path.exists(audit_log_csv):
                    audit_df = pd.read_csv(audit_log_csv)
                else:
                    audit_df = pd.DataFrame(columns=["Timestamp", "Username", "Action"])
                audit_df = audit_df.append(entry, ignore_index=True)
                audit_df.to_csv(audit_log_csv, index=False)

            log_activity(username_input, "User logged in")

            # Secure Data Sharing (role-based)
            st.subheader("🔒 Secure Data Sharing")

            if user_role in ["Manager", "Administrator"]:
                with st.expander("📤 Upload Secure Files"):
                    uploaded_file = st.file_uploader("Choose file to upload securely")
                    if uploaded_file:
                        file_path = os.path.join(SHARED_DIR, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        st.success(f"File '{uploaded_file.name}' uploaded securely.")
                        log_activity(username_input, f"Uploaded file: {uploaded_file.name}")
            else:
                st.info("File uploading restricted to Managers and Administrators.")

            st.subheader("📁 Secure Files Available")
            available_files = os.listdir(SHARED_DIR)

            if available_files:
                for file in available_files:
                    file_path = os.path.join(SHARED_DIR, file)
                    with open(file_path, "rb") as f:
                        st.download_button(f"📥 Download {file}", f, file_name=file)
                        log_activity(username_input, f"Accessed file: {file}")
            else:
                st.info("No secure files available.")

        else:
            st.sidebar.error("Incorrect password.")
    else:
        st.sidebar.error("Username not found.")

# Main Page: User Accounts & Audit Logs
st.subheader("👥 User Accounts Overview")
if not users_df.empty:
    display_df = users_df[["Username", "Full_Name", "Role", "Date_Created", "Last_Login"]]
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("No user accounts found.")

st.subheader("📑 Recent Audit Trail")
if os.path.exists(audit_log_csv):
    audit_df = pd.read_csv(audit_log_csv)
    st.dataframe(audit_df.tail(50), use_container_width=True)
else:
    st.info("Audit trail currently empty.")

# Placeholder for future enhancements
st.subheader("🚧 Future Security Enhancements")
st.info("Upcoming: Password reset, account management, enhanced session security.")