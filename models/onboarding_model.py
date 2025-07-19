
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

Base = declarative_base()

class InstrumentOnboarding(Base):
    __tablename__ = "instrument_onboarding"

    id = Column(Integer, primary_key=True)
    serial = Column(String, nullable=False)
    brand = Column(String)
    model = Column(String)
    detectors = Column(Text)  # Store as comma-separated string
    column = Column(String)
    method = Column(String)
    sample_types = Column(Text)
    last_cal = Column(String)
    frequency = Column(String)
    image_path = Column(String)
    status = Column(String, default="incomplete")
    created_at = Column(DateTime, default=datetime.utcnow)
