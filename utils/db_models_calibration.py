from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class GCCalibration(Base):
    __tablename__ = "gc_calibrations"

    id = Column(Integer, primary_key=True)
    instrument_serial = Column(String(100), nullable=False)
    method = Column(String(50))
    compound = Column(String(100))
    response_factor = Column(Float)
    calibration_date = Column(DateTime, default=datetime.utcnow)
    analyst = Column(String(100))
    status = Column(String(20))  # e.g., "Pass", "Fail", "Warning"
    notes = Column(Text)
