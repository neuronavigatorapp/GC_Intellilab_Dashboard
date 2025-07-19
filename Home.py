import streamlit as st

# Set page config
st.set_page_config(
    page_title="GC IntelliLab",
    layout="centered",  # Better for mobile by default
    initial_sidebar_state="collapsed"  # Hides sidebar on mobile
)

# Mobile-friendly CSS overrides
st.markdown("""
    <style>
    ul {
        padding-left: 1.2rem;
        line-height: 1.8;
    }
    li {
        font-size: 1.1rem;
    }
    .block-container {
        padding-top: 2rem;
    }
    @media screen and (max-width: 600px) {
        h1 {
            font-size: 1.8rem !important;
        }
        li {
            font-size: 1rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 style='text-align: center;'>IntelliLab</h1>", unsafe_allow_html=True)

# Intro
st.markdown("""
<div style="text-align: center; margin-bottom: 1.5rem;">
    <p style="font-size: 1.05rem;">Access GC modules using the sidebar or tap the section below:</p>
</div>
""", unsafe_allow_html=True)

# Top Button Navigation
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/1_Instrument_Management.py", label="Instruments", icon="🧪")
with col2:
    st.page_link("pages/3_QC_Calibration.py", label="QC", icon="📏")
with col3:
    st.page_link("pages/4_Troubleshooting.py", label="Troubleshoot", icon="🛠️")

# Section Overview
st.markdown("""
<div style="max-width: 600px; margin: 2rem auto 0 auto; font-size: 1.05rem;">
<ul>
  <li><strong>Instrument Management</strong> — Configure and track GC systems</li>
  <li><strong>Inventory</strong> — Monitor columns, valves, detectors, etc.</li>
  <li><strong>QC & Calibration</strong> — Log calibrations and validate performance</li>
  <li><strong>Troubleshooting</strong> — Diagnose known faults and log new ones</li>
  <li><strong>Maintenance</strong> — Schedule and record preventative service</li>
  <li><strong>Reports & AI Assistant</strong> — Generate reports or ask AI for help</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Sidebar reminder
st.info("📱 On mobile? Tap the ☰ icon in the corner to open the module menu.", icon="📲")
