from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base


class SafetyReport(Base):
    __tablename__ = "safety_reports"

    id = Column(Integer, primary_key=True, index=True)

    report = Column(String, nullable=False)

    sif_potential = Column(String)
    risk_level = Column(String)
    life_saving_rule = Column(String)
    hazard = Column(String)
    barrier_failure = Column(String)
    confidence = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)