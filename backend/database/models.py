from sqlalchemy import Column, Float, Integer
from .database import Base

class RiskRecord(Base):
    __tablename__ = "risk_records"

    id = Column(Integer, primary_key=True, index=True)
    news_negative_pct = Column(Float)
    keyword_score = Column(Float)
    weather_risk = Column(Float)
    port_delay_index = Column(Float)
    supplier_concentration = Column(Float)
    hist_delay = Column(Float)
    risk_score = Column(Float)
