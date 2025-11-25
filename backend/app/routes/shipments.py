# backend/app/routes/shipments.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import client
from datetime import datetime

router = APIRouter()

class ShipmentIn(BaseModel):
    shipment_id: str
    order_id: str
    origin: str
    destination: str
    status: str = "in_transit"

@router.post("/shipments")
def create_shipment(payload: ShipmentIn):
    col = client["supply"]["shipments"]
    doc = payload.dict()
    doc["created_at"] = datetime.utcnow().isoformat()
    col.insert_one(doc)
    return {"status": "ok", "shipment_id": payload.shipment_id}

@router.get("/shipments/{shipment_id}")
def get_shipment(shipment_id: str):
    col = client["supply"]["shipments"]
    doc = col.find_one({"shipment_id": shipment_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Shipment not found")
    doc.pop("_id", None)
    return doc

@router.patch("/shipments/{shipment_id}")
def update_shipment(shipment_id: str, status: str):
    col = client["supply"]["shipments"]
    res = col.update_one({"shipment_id": shipment_id}, {"$set": {"status": status}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return {"status": "updated"}
