import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ✅ Fixed module import path
from models.db_models_inventory import GCConsumable, Base

# 1️⃣ Connect to DB
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

# 2️⃣ Page Setup
st.set_page_config(page_title="📦 Inventory Manager", layout="wide")
st.title("📦 GC Consumable Inventory")

# 3️⃣ Add Consumable Form
with st.expander("➕ Add New Consumable", expanded=False):
    with st.form("add_inventory"):
        name = st.text_input("Item Name", placeholder="e.g. Agilent Gold Seal")
        category = st.selectbox("Category", [
            "Inlet", "Detector", "Column", "Autosampler", "Valve", "Standards", "Gas Purifier", "Other"
        ])
        quantity = st.number_input("Quantity", 0.0)
        units = st.selectbox("Units", ["pcs", "mL", "g", "pack", "box"])
        reorder = st.number_input("Reorder Point", 0.0)
        linked_instrument = st.text_input("Linked Instrument Serial (optional)")
        notes = st.text_area("Notes")

        submit = st.form_submit_button("Add Item")

    if submit:
        item = GCConsumable(
            name=name,
            category=category,
            quantity=quantity,
            units=units,
            reorder_point=reorder,
            linked_instrument=linked_instrument,
            notes=notes
        )
        session.add(item)
        session.commit()
        st.success(f"{name} added to inventory.")

# 4️⃣ View Current Inventory
st.subheader("📋 Current Stock")

items = session.query(GCConsumable).all()
if not items:
    st.info("No inventory items yet.")
else:
    data = []
    for i in items:
        low = i.quantity <= i.reorder_point
        data.append({
            "Name": i.name,
            "Category": i.category,
            "Qty": i.quantity,
            "Units": i.units,
            "Reorder @": i.reorder_point,
            "Linked Instrument": i.linked_instrument,
            "⚠️ Low Stock": "🔴" if low else "",
            "Notes": i.notes
        })

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

session.close()
