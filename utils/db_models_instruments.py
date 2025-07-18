from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GCInstrument(Base):
    __tablename__ = "gc_instruments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    serial_number = Column(String(100), unique=True)
    model = Column(String(50))
    channels = Column(String(20))  # "Single" or "Dual"
    detectors = Column(String(100))  # e.g., "FID,TCD"
    methods_supported = Column(String(200))  # e.g., "D6730,D2163"
    location = Column(String(100))
    notes = Column(Text)
