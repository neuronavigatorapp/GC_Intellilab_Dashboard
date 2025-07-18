from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class GCTroubleshooting(Base):
    __tablename__ = "gc_troubleshooting"

    id = Column(Integer, primary_key=True)
    instrument_serial = Column(String(100))
    method = Column(String(50))
    detector = Column(String(50))
    fault_type = Column(String(100))  # e.g. Tailing, Ghost Peak, No Ignition
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)
    resolution = Column(Text)
    operator = Column(String(100))
    status = Column(String(20))  # Open, Closed, Escalated
