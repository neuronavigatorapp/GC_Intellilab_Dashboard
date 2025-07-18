from sqlalchemy import Column, Integer, String, Float, DateTime, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class GCDiagnostic(Base):
    __tablename__ = "gc_diagnostics"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    inlet_temp = Column(Float)
    oven_start = Column(Float)
    ramp_rate = Column(Float)
    oven_final = Column(Float)
    hold_time = Column(Float)
    flow_rate = Column(Float)
    column_type = Column(String(50))
    detector = Column(String(50))
    user_question = Column(Text)
    ai_response = Column(Text)

# ---- Setup engine and session ----
DATABASE_PATH = "sqlite:///./data/shared_files/intellilab_gc.db"  # or change path as needed
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# ---- Create the table ----
def init_db():
    Base.metadata.create_all(bind=engine)
