from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class GCConsumable(Base):
    __tablename__ = "gc_consumables"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    quantity = Column(Float)
    units = Column(String)
    reorder_point = Column(Float)
    linked_instrument = Column(String)
    notes = Column(String)
