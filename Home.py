# 1️⃣ Imports
import streamlit as st
from utils.db_models import init_db  # Compound DB init

from db_models_instruments import Base as InstrumentBase
from db_models_inventory import Base as InventoryBase
from db_models_calibration import Base as CalibrationBase
from db_models_troubleshooting import Base as TroubleshootingBase
from db_models_maintenance import Base as MaintenanceBase  # ✅ New

from sqlalchemy import create_engine

# 2️⃣ Initialize compound DB
init_db()

# 3️⃣ Set up engine
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})

# 4️⃣ Create all supplemental tables
InstrumentBase.metadata.create_all(engine)
InventoryBase.metadata.create_all(engine)
CalibrationBase.metadata.create_all(engine)
TroubleshootingBase.metadata.create_all(engine)
MaintenanceBase.metadata.create_all(engine)  # ✅ Maintenance log table

# 5️⃣ Streamlit UI
st.set_page_config(page_title="GC IntelliLab Home", layout="wide")
st.title("🧬 GC IntelliLab Dashboard")

st.markdown("""
Welcome to **GC IntelliLab Dashboard**!  
Use the sidebar on the left to navigate between different modules:
- 🧪 Instrument Management  
- 📦 Inventory Management  
- 🎯 QC & Calibration  
- 🔍 Troubleshooting Logs  
- 🛠 Maintenance Logs  
- 📄 Reporting & Documentation  
""")
