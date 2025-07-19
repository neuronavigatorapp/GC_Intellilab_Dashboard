from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class GCTroubleshooting(Base):
    __tablename__ = "gc_troubleshooting"

    id = Column(Integer, primary_key=True)
    instrument_serial = Column(String)
    method = Column(String)
    detector = Column(String)
    fault_type = Column(String)
    description = Column(String)
    resolution = Column(String)
    operator = Column(String)
    status = Column(String)
    date = Column(DateTime)
