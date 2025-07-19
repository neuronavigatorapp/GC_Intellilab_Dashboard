
import streamlit as st
import cv2
import numpy as np
import os
from glob import glob
from PIL import Image

st.set_page_config(page_title="🔍 Peak Overlay Visualizer", layout="centered")
st.markdown("<h1 style='text-align: center;'>🔍 Peak Overlay Viewer</h1>", unsafe_allow_html=True)

# Locate uploaded chromatograms
img_folder = "./data/shared_files"
images = sorted(glob(os.path.join(img_folder, "*_chromatogram.png")))

if len(images) < 2:
    st.warning("Upload at least two chromatograms via AI Home Mode before using the overlay viewer.")
    st.stop()

selected_imgs = st.multiselect("Select chromatograms to compare:", images, default=images[:2])

if len(selected_imgs) < 2:
    st.info("Select at least two chromatograms to view overlay.")
    st.stop()

# Load and normalize sizes
loaded_imgs = [cv2.imread(img, cv2.IMREAD_GRAYSCALE) for img in selected_imgs]
min_height = min(img.shape[0] for img in loaded_imgs)
resized_imgs = [cv2.resize(img, (img.shape[1], min_height)) for img in loaded_imgs]

# Stack for overlay
stacked = np.stack(resized_imgs, axis=-1)
overlay = np.mean(stacked, axis=-1).astype(np.uint8)

# Convert to color and draw contours on each layer
overlay_color = cv2.cvtColor(overlay, cv2.COLOR_GRAY2BGR)
colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0)]

for idx, img in enumerate(resized_imgs):
    _, thresh = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if h > 20 and w < 100:
            cv2.rectangle(overlay_color, (x, y), (x+w, y+h), colors[idx % len(colors)], 1)

st.image(overlay_color, caption="Overlay of Selected Chromatograms", use_column_width=True)
st.markdown("Each color represents a different chromatogram. Boxes show peak positions.")
