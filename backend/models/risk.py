from pydantic import BaseModel

class RiskData(BaseModel):
    news_negative_pct: float
    keyword_score: float
    weather_risk: float
    port_delay_index: float
    supplier_concentration: float
    hist_delay: float
    risk_score: float
