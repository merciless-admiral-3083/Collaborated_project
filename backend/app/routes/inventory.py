# backend/app/routes/inventory.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import client
from datetime import datetime

router = APIRouter()

class InventoryIn(BaseModel):
    sku: str
    location: str
    qty: int

@router.post("/inventory")
def create_inventory(item: InventoryIn):
    col = client["supply"]["inventory"]
    doc = item.dict()
    doc["updated_at"] = datetime.utcnow().isoformat()
    col.insert_one(doc)
    return {"status": "ok"}

@router.get("/inventory/{sku}")
def get_inventory(sku: str):
    col = client["supply"]["inventory"]
    doc = col.find_one({"sku": sku})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    doc.pop("_id", None)
    return doc

@router.patch("/inventory/{sku}")
def adjust_inventory(sku: str, delta: int):
    col = client["supply"]["inventory"]
    res = col.update_one({"sku": sku}, {"$inc": {"qty": delta}, "$set": {"updated_at": datetime.utcnow().isoformat()}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "updated"}
