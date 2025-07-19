# 1️⃣ Imports
import streamlit as st
import plotly.express as px
from utils.retention_model import (
    get_available_methods,
    load_compound_data,
    simulate_retention_times,
    generate_chromatogram,
    get_method_reference_url
)
from utils.pdf_exporter import generate_retention_pdf

# 2️⃣ Page Setup
st.set_page_config(page_title="🧪 GC Simulator", layout="centered")

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

st.title("🧪 GC Retention Simulator with Method-Aware Compounds")

# 3️⃣ GC Method & Parameters Input Form
with st.form("simulator"):
    st.subheader("GC Method & Parameters")

    method = st.selectbox("Select Method", get_available_methods())
    ref_url = get_method_reference_url(method)
    if ref_url:
        st.markdown(f"🔗 [View ASTM {method} Overview]({ref_url})")

    oven_start = st.number_input("Oven Start Temp (°C)", 30, 200, 40)
    oven_final = st.number_input("Oven Final Temp (°C)", 100, 400, 260)
    ramp_rate = st.number_input("Ramp Rate (°C/min)", 1, 100, 10)
    flow_rate = st.number_input("Flow Rate (mL/min)", 0.1, 10.0, 1.2)
    run_time = st.number_input("Run Time (min)", 5, 60, 30)

    submit = st.form_submit_button("Run Simulation")

# 4️⃣ Run Simulation Logic
if submit:
    compound_df = load_compound_data(method)

    if compound_df.empty:
        st.warning("No compounds found for this method.")
    else:
        rt_df = simulate_retention_times(compound_df, oven_start, ramp_rate, flow_rate)
        chroma_df = generate_chromatogram(rt_df, run_time=run_time)

        # 5️⃣ Plot Chromatogram
        st.subheader("📊 Simulated Chromatogram")
        fig = px.line(chroma_df, x="Time (min)", y="Detector Response")
        st.plotly_chart(fig, use_container_width=True)

        # 6️⃣ Show Retention Table + Download Option
        st.subheader("🧪 Retention Table")
        st.dataframe(rt_df, use_container_width=True)

        # 7️⃣ Export Buttons
        st.download_button(
            "📥 Download Retention Table as CSV",
            rt_df.to_csv(index=False),
            "retention_table.csv",
            "text/csv"
        )

        # 8️⃣ PDF Export
        pdf_path = generate_retention_pdf(rt_df)
        with open(pdf_path, "rb") as f:
            st.download_button("🧾 Export as PDF", f.read(), "retention_report.pdf", "application/pdf")