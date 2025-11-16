from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CountryData(BaseModel):
    country: str

@app.get("/api/hello")
def read_root():
    return {"message": "Backend connected successfully 🚀"}

@app.post("/api/analyze")
def analyze_data(data: CountryData):
    return {"country": data.country, "risk_score": 72.4, "status": "Moderate risk"}

@app.get("/api/global_summary")
def get_summary():
    return {
        "total_ports": 120,
        "alerts_active": 8,
        "avg_risk_score": 64.3
    }
