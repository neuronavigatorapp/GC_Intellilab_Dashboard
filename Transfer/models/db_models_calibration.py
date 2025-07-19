from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

Base = declarative_base()

class GCCalibration(Base):
    __tablename__ = "gc_calibrations"

    id = Column(Integer, primary_key=True)
    instrument_serial = Column(String)
    method = Column(String)
    compound = Column(String)
    response_factor = Column(Float)
    status = Column(String)
    analyst = Column(String)
    notes = Column(String)
    calibration_date = Column(DateTime)
