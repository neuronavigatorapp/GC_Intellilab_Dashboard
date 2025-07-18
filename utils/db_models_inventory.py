from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class GCConsumable(Base):
    __tablename__ = "gc_consumables"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))  # e.g. Inlet, Column, Detector, Standards, Syringe
    quantity = Column(Float, default=0)
    units = Column(String(20), default="pcs")  # e.g. pcs, mL, g
    reorder_point = Column(Float, default=0)
    linked_instrument = Column(String(100))  # Optional: match serial_number
    last_updated = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
