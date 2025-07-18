import streamlit as st
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Inventory Management", layout="wide")
st.title("📦 GC Inventory Management & AI Forecasting")

# Data directory
DATA_DIR = "../data/inventory"
os.makedirs(DATA_DIR, exist_ok=True)
inventory_csv = os.path.join(DATA_DIR, "gc_inventory.csv")

# Load existing inventory data or create empty dataframe
if os.path.exists(inventory_csv):
    inventory_df = pd.read_csv(inventory_csv)
else:
    inventory_df = pd.DataFrame(columns=[
        "Consumable_Category", "Item_Name", "Agilent_Part_Number",
        "Quantity_Available", "Reorder_Level", "Last_Updated", "Daily_Usage_Rate"
    ])

# Sidebar: Add Inventory Item
st.sidebar.header("➕ Add New Inventory Item")

with st.sidebar.form("new_inventory_form"):
    category = st.selectbox("Consumable Category", [
        "Inlet Consumables", "Column Consumables", "FID Detector Consumables",
        "TCD Detector Consumables", "SCD Detector Consumables",
        "Methanizer Consumables", "Autosampler Consumables",
        "Valve Consumables", "Misc Lab Supplies", "Calibration/QC Standards"
    ])
    item_name = st.text_input("Item Name")
    part_number = st.text_input("Agilent Part Number")
    quantity = st.number_input("Quantity Available", min_value=0)
    reorder_level = st.number_input("Reorder Threshold", min_value=0)
    daily_usage_rate = st.number_input("Estimated Daily Usage", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("Save Item")

    if submitted:
        new_item = {
            "Consumable_Category": category,
            "Item_Name": item_name,
            "Agilent_Part_Number": part_number,
            "Quantity_Available": quantity,
            "Reorder_Level": reorder_level,
            "Daily_Usage_Rate": daily_usage_rate,
            "Last_Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        inventory_df = inventory_df.append(new_item, ignore_index=True)
        inventory_df.to_csv(inventory_csv, index=False)
        st.sidebar.success(f"Item '{item_name}' added successfully!")

# Main Inventory Overview
st.subheader("📋 Inventory Overview & Forecast")

if not inventory_df.empty:
    inventory_df["Days_to_Reorder"] = (inventory_df["Quantity_Available"] - inventory_df["Reorder_Level"]) / inventory_df["Daily_Usage_Rate"]
    inventory_df["Reorder_Date"] = pd.to_datetime(inventory_df["Last_Updated"]) + inventory_df["Days_to_Reorder"].apply(lambda x: timedelta(days=max(x,0)))

    st.dataframe(inventory_df[["Item_Name", "Quantity_Available", "Reorder_Level", "Daily_Usage_Rate", "Days_to_Reorder", "Reorder_Date"]], use_container_width=True)

    # Reorder Alerts
    st.subheader("⚠️ Items Requiring Immediate Attention")
    critical_items = inventory_df[inventory_df["Days_to_Reorder"] <= 7]  # Next 7 days
    if not critical_items.empty:
        st.dataframe(critical_items[["Item_Name", "Quantity_Available", "Days_to_Reorder", "Reorder_Date"]], use_container_width=True)
    else:
        st.success("No immediate reordering necessary.")

    # Inventory Forecasting Plot
    st.subheader("📊 Inventory Forecast")
    forecast_days = 30
    forecast_dates = [datetime.today() + timedelta(days=i) for i in range(forecast_days)]

    forecast_df = pd.DataFrame({"Date": forecast_dates})
    for _, row in inventory_df.iterrows():
        usage_projection = row["Quantity_Available"] - row["Daily_Usage_Rate"] * np.arange(forecast_days)
        forecast_df[row["Item_Name"]] = np.maximum(usage_projection, 0)

    forecast_melted = forecast_df.melt(id_vars=["Date"], var_name="Item", value_name="Projected Quantity")

    fig = px.line(forecast_melted, x="Date", y="Projected Quantity", color="Item", markers=True,
                  title="30-Day Inventory Level Forecast", labels={"Projected Quantity": "Quantity"})
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Inventory is currently empty. Add new items from the sidebar.")

# Update Inventory Quantities
with st.expander("🔄 Update Inventory Quantity"):
    if not inventory_df.empty:
        item_update = st.selectbox("Select Item to Update", inventory_df["Item_Name"])
        new_quantity = st.number_input("New Quantity Available", min_value=0, step=1)
        if st.button("Update Quantity"):
            inventory_df.loc[inventory_df["Item_Name"] == item_update, ["Quantity_Available", "Last_Updated"]] = [new_quantity, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            inventory_df.to_csv(inventory_csv, index=False)
            st.success(f"Quantity updated for '{item_update}'. Refresh to see updated forecasts.")
    else:
        st.warning("No items available to update.")
