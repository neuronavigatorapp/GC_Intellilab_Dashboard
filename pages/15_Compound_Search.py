# 1️⃣ Imports
import streamlit as st
import pandas as pd
import os

# 2️⃣ Load the Compound Database
DB_PATH = os.path.join("data", "shared_files", "GC_Master_Compound_Database_with_Scaffolds.csv")

@st.cache_data
def load_compound_db():
    return pd.read_csv(DB_PATH)

# 3️⃣ Page Setup
st.set_page_config(page_title="🔍 Compound Browser", layout="centered")

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

st.title("🔍 Compound Search & Viewer")

# 4️⃣ Load Data
df = load_compound_db()
all_methods = ["All"] + sorted(df["Method"].dropna().unique())

# 5️⃣ Sidebar Filters
method = st.selectbox("Filter by Method", all_methods)
query = st.text_input("Search by Compound Name, Class, or Formula")

# 6️⃣ Apply Filters
filtered = df.copy()

if method != "All":
    filtered = filtered[filtered["Method"] == method]

if query:
    query = query.lower()
    filtered = filtered[
        filtered["Compound"].str.lower().str.contains(query) |
        filtered["Class"].str.lower().str.contains(query) |
        filtered["Formula"].str.lower().str.contains(query)
    ]

# 7️⃣ Display Table
st.dataframe(filtered.sort_values("Compound").reset_index(drop=True), use_container_width=True)

# 8️⃣ Optional CSV Download
if not filtered.empty:
    st.download_button(
        "📥 Download Filtered Table as CSV",
        filtered.to_csv(index=False),
        "filtered_compounds.csv",
        "text/csv"
    )