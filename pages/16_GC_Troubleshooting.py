# 1️⃣ Imports
import streamlit as st
import plotly.graph_objects as go
from utils.retention_model import (
    get_available_methods,
    load_compound_data,
    simulate_retention_times,
    generate_chromatogram
)
from utils.gc_faults import GC_FAULT_METADATA  # 🔧 New: descriptive metadata

# 2️⃣ Detector-specific GC faults
GC_FAULTS = {
    "FID": ["None", "Tailing", "Signal Loss", "Ghost Peaks", "No Ignition", "Flame Blowout Mid-run"],
    "TCD": ["None", "Negative Peaks", "Baseline Drift", "Filament Failure", "Carrier Gas Leak"],
    "SCD": ["None", "Plasma Disruption", "Dual Burner Drift", "Sulfur Carryover", "Signal Saturation"],
    "FID + Methanizer": ["None", "Catalyst Loss", "Catalyst Overheat", "Injector Leak"]
}

# 3️⃣ Setup page
st.set_page_config(page_title="🔧 GC Troubleshooting Viewer", layout="centered")

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

st.title("🔧 GC Fault Simulator: Detector-Aware Chromatograms")

# 4️⃣ Detector & fault selection
col1, col2 = st.columns(2)
with col1:
    detector = st.selectbox("Detector Type", list(GC_FAULTS.keys()))
with col2:
    issue = st.selectbox("Simulated Fault", GC_FAULTS[detector])

# 5️⃣ GC Method + Parameters
with st.form("troubleshoot"):
    st.subheader("GC Method Parameters")
    method = st.selectbox("Select GC Method", get_available_methods())
    oven_start = st.number_input("Oven Start Temp (°C)", 30, 200, 40)
    ramp_rate = st.number_input("Ramp Rate (°C/min)", 1, 100, 10)
    flow_rate = st.number_input("Flow Rate (mL/min)", 0.1, 10.0, 1.2)
    run_time = st.number_input("Total Run Time (min)", 5, 60, 25)
    submit = st.form_submit_button("Simulate")

# 6️⃣ Run Simulation and Show Side-by-Side Charts
if submit:
    compounds = load_compound_data(method)
    if compounds.empty:
        st.warning("No compounds available for this method.")
    else:
        rt_df = simulate_retention_times(compounds, oven_start, ramp_rate, flow_rate)

        healthy = generate_chromatogram(rt_df, run_time)
        faulted = generate_chromatogram(rt_df, run_time, issue=None if issue == "None" else issue)

        st.subheader(f"🆚 Healthy vs Faulted: {issue}")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Normal Chromatogram")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=healthy["Time (min)"], y=healthy["Detector Response"], name="Normal"))
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(f"### ⚠️ Fault: {issue}")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=faulted["Time (min)"], y=faulted["Detector Response"], name="Faulted"))
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)

        # 7️⃣ Tooltip for cause + fix
        if issue in GC_FAULT_METADATA:
            st.markdown("---")
            st.info(f"""
**🔎 Likely Cause:** {GC_FAULT_METADATA[issue]['Cause']}

**🛠 Suggested Fix:** {GC_FAULT_METADATA[issue]['Fix']}
""")

        # 8️⃣ Preview AI Prompt (for integration with LLM later)
        st.markdown("---")
        st.subheader("🧠 AI Diagnostic Prompt Preview")
        prompt = f"""A GC {detector} run with method {method} showed signs of "{issue}".
Oven: {oven_start} °C start, Ramp {ramp_rate} °C/min, Flow {flow_rate} mL/min.
Simulated result includes compound elution from {compounds['Compound'].iloc[0]} to {compounds['Compound'].iloc[-1]}.

What are the most likely root causes for this issue, and what steps should a lab tech take to confirm and resolve it?
"""
        st.code(prompt, language="markdown")