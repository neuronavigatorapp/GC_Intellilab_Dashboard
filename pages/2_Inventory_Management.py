import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page configuration
st.set_page_config(page_title="Inventory Management", layout="wide")
st.title("📦 GC Inventory Management (Agilent Consumables)")

# Create directory for data persistence
DATA_DIR = "../data/inventory"
os.makedirs(DATA_DIR, exist_ok=True)
inventory_csv = os.path.join(DATA_DIR, "gc_inventory.csv")

# Load existing inventory data or create an empty dataframe
if os.path.exists(inventory_csv):
    inventory_df = pd.read_csv(inventory_csv)
else:
    inventory_df = pd.DataFrame(columns=[
        "Consumable_Category", "Item_Name", "Agilent_Part_Number",
        "Quantity_Available", "Reorder_Level", "Last_Updated"
    ])

# Sidebar: Add New Inventory Item
st.sidebar.header("➕ Add New Inventory Item")

with st.sidebar.form("new_inventory_form"):
    consumable_category = st.selectbox("Consumable Category", [
        "Inlet Consumables", "Column Consumables", "FID Detector Consumables",
        "TCD Detector Consumables", "SCD Detector Consumables",
        "Methanizer Consumables", "Autosampler Consumables",
        "Valve Consumables", "Misc Lab Supplies", "Calibration/QC Standards"
    ])
    item_name = st.text_input("Item Name (Description)")
    part_number = st.text_input("Agilent Part Number")
    quantity_available = st.number_input("Quantity Available", min_value=0, step=1)
    reorder_level = st.number_input("Reorder Threshold", min_value=0, step=1)
    submitted = st.form_submit_button("Save Item")

    if submitted:
        new_item = {
            "Consumable_Category": consumable_category,
            "Item_Name": item_name,
            "Agilent_Part_Number": part_number,
            "Quantity_Available": quantity_available,
            "Reorder_Level": reorder_level,
            "Last_Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        inventory_df = inventory_df.append(new_item, ignore_index=True)
        inventory_df.to_csv(inventory_csv, index=False)
        st.sidebar.success(f"Inventory item '{item_name}' saved successfully!")

# Main Page: Inventory Overview
st.subheader("📋 Current Inventory Status")

if not inventory_df.empty:
    st.dataframe(inventory_df, use_container_width=True)

    # Highlight items below reorder threshold
    st.subheader("⚠️ Items Below Reorder Level")
    low_stock_df = inventory_df[inventory_df["Quantity_Available"] <= inventory_df["Reorder_Level"]]
    if not low_stock_df.empty:
        st.dataframe(low_stock_df, use_container_width=True)
    else:
        st.success("All items currently above reorder levels.")
else:
    st.info("No inventory items found. Add items using the sidebar.")

# Allow updating inventory quantities
with st.expander("🔄 Update Inventory Quantity"):
    if not inventory_df.empty:
        update_item = st.selectbox("Select Item to Update", inventory_df["Item_Name"].unique())
        new_quantity = st.number_input("New Quantity Available", min_value=0, step=1)
        if st.button("Update Quantity"):
            inventory_df.loc[inventory_df["Item_Name"] == update_item, "Quantity_Available"] = new_quantity
            inventory_df.loc[inventory_df["Item_Name"] == update_item, "Last_Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            inventory_df.to_csv(inventory_csv, index=False)
            st.success(f"Inventory quantity updated for '{update_item}'. Refresh to see updated values.")
    else:
        st.warning("No inventory items available to update.")
