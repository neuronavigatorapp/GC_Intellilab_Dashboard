import streamlit as st
import cv2
import numpy as np
import os
from glob import glob

# Page setup
st.set_page_config(page_title="📈 Chromatogram Analyzer", layout="centered")
st.markdown("<h1 style='text-align: center;'>📈 Chromatogram Analyzer</h1>", unsafe_allow_html=True)

# File discovery
image_folder = "./data/shared_files"
image_files = sorted(glob(os.path.join(image_folder, "*_chromatogram.png")))

if not image_files:
    st.warning("No chromatogram screenshots found. Upload one through AI Home Mode.")
    st.stop()

# File selector
selected_image = st.selectbox("Select a chromatogram to analyze:", image_files)
st.image(selected_image, caption="Original Screenshot", use_column_width=True)

# Load image
img = cv2.imread(selected_image)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)
_, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
peak_img = img.copy()
peaks = []

# Retention time calibration
st.markdown("### ⏱️ Retention Time Calibration")
col1, col2 = st.columns(2)
with col1:
    rt_start = st.number_input("Retention Time Start (left edge)", min_value=0.0, value=0.0)
with col2:
    rt_end = st.number_input("Retention Time End (right edge)", min_value=0.1, value=20.0)

width = img.shape[1]
scale = (rt_end - rt_start) / width if width > 0 else 1.0

# Draw and extract peaks
for i, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)
    if h > 20 and w < 100:
        cv2.rectangle(peak_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        rt_estimate = round(rt_start + (x * scale), 2)
        cv2.putText(peak_img, f"{rt_estimate} min", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
        peaks.append((rt_estimate, w, h))

# Output
st.image(cv2.cvtColor(peak_img, cv2.COLOR_BGR2RGB), caption="Detected Peaks with Retention Time", use_column_width=True)
st.markdown("### 🧾 Summary")
st.markdown(f"- **Detected Peaks:** {len(peaks)}")

if peaks:
    rt_list = ", ".join([f"{p[0]} min" for p in sorted(peaks, key=lambda x: x[0])[:8]])
    st.markdown(f"- **Estimated RTs:** {rt_list}" + ("..." if len(peaks) > 8 else ""))
else:
    st.info("No peaks detected — check image contrast or clarity.")
