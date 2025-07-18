from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class GCMaintenance(Base):
    __tablename__ = "gc_maintenance"

    id = Column(Integer, primary_key=True)
    instrument_serial = Column(String(100), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    service_type = Column(String(100))  # e.g. "PM", "Corrective", "Calibration", "Emergency"
    parts_replaced = Column(Text)
    technician = Column(String(100))
    notes = Column(Text)
