import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests

# Page configuration
st.set_page_config(page_title="GC Sandbox Simulation", layout="wide")
st.title("🧪 GC Sandbox: AI-Driven Diagnostics")

# Sidebar: GC Simulation Parameters
st.sidebar.header("Simulation Parameters")
col_type = st.sidebar.selectbox("Column Type", ["DB-1", "DB-5", "MAPD", "LowOx", "Packed"])
initial_temp = st.sidebar.slider("Initial Oven Temp (°C)", 30, 200, 50)
final_temp = st.sidebar.slider("Final Oven Temp (°C)", 100, 350, 250)
ramp_rate = st.sidebar.slider("Ramp Rate (°C/min)", 1, 50, 10)
carrier_gas_flow = st.sidebar.slider("Carrier Gas Flow (mL/min)", 0.1, 10.0, 1.0)

# Sidebar: Troubleshooting Scenario Toggles
st.sidebar.header("Troubleshooting Simulations")
col_issue = st.sidebar.checkbox("Column Installation Error")
phase_depletion = st.sidebar.checkbox("Column Phase Depletion")
epc_issue = st.sidebar.checkbox("Carrier Gas EPC Failure")
detector_issue = st.sidebar.checkbox("Detector Issue (FID, TCD, SCD, Methanizer)")
contaminant_carryover = st.sidebar.checkbox("Contaminant Carryover")

# Run Simulation Button
simulate_button = st.sidebar.button("Run GC Simulation & AI Diagnostics")

if simulate_button:
    time_axis = np.linspace(0, 30, 5000)
    baseline_noise = np.random.normal(0, 0.5, len(time_axis))

    def gaussian_peak(center, width, height):
        return height * np.exp(-((time_axis - center) ** 2) / (2 * width ** 2))

    peaks = gaussian_peak(5, 0.1, 100) + gaussian_peak(10, 0.2, 200) + gaussian_peak(15, 0.15, 150)

    # Apply troubleshooting scenarios
    anomalies_detected = []
    if col_issue:
        peaks *= np.exp(-0.05 * time_axis)
        baseline_noise += np.random.normal(2, 0.3, len(time_axis))
        anomalies_detected.append("Column Installation Issue (peak tailing)")

    if phase_depletion:
        peaks *= 0.6
        baseline_noise += np.linspace(0, 10, len(time_axis))
        anomalies_detected.append("Phase Depletion (reduced sensitivity, baseline drift)")

    if epc_issue:
        peaks = np.roll(peaks, 200)
        baseline_noise += np.random.normal(3, 1.0, len(time_axis))
        anomalies_detected.append("EPC Flow Issue (retention time shift)")

    if detector_issue:
        peaks *= 0.3
        baseline_noise += np.random.normal(5, 1.5, len(time_axis))
        anomalies_detected.append("Detector Sensitivity Issue")

    if contaminant_carryover:
        peaks += gaussian_peak(7, 0.3, 300)
        anomalies_detected.append("Contaminant Carryover Detected")

    chromatogram = peaks + baseline_noise

    # Plot Simulated Chromatogram
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_axis, y=chromatogram, mode='lines', name='Simulated Chromatogram'))
    fig.update_layout(title="GC Troubleshooting & AI Simulation", xaxis_title="Time (min)", yaxis_title="Intensity")
    st.plotly_chart(fig, use_container_width=True)

    # AI-driven Anomaly Detection
    with st.spinner("Running AI Diagnostics..."):
        ai_payload = {
            "issue_description": ", ".join(anomalies_detected) if anomalies_detected else "No obvious anomalies",
            "recent_actions": f"Column: {col_type}, Initial Temp: {initial_temp}, Final Temp: {final_temp}, Ramp: {ramp_rate}, Flow: {carrier_gas_flow}"
        }
        response = requests.post("http://localhost:8000/ai-troubleshoot-advanced/", json=ai_payload)

        if response.ok:
            ai_diagnostics = response.json()["troubleshooting_steps"]
            st.subheader("🤖 AI Diagnostic Recommendations")
            st.success(ai_diagnostics)
        else:
            st.error("AI Diagnostic Service currently unavailable.")

else:
    st.info("Adjust parameters and troubleshooting scenarios, then click 'Run GC Simulation & AI Diagnostics'.")
