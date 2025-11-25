# backend/app/routes/orders.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.db import client
from datetime import datetime

router = APIRouter()

class OrderIn(BaseModel):
    order_id: str
    country: str
    supplier: str
    qty: int
    eta: str = None

@router.post("/orders")
def create_order(payload: OrderIn):
    db = client["supply"]
    col = db["orders"]
    doc = payload.dict()
    doc["created_at"] = datetime.utcnow().isoformat()
    col.insert_one(doc)
    return {"status": "ok", "order_id": payload.order_id}

@router.get("/orders/{order_id}")
def get_order(order_id: str):
    db = client["supply"]
    col = db["orders"]
    doc = col.find_one({"order_id": order_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Order not found")
    doc.pop("_id", None)
    return doc

@router.get("/orders")
def list_orders(limit: int = 50):
    col = client["supply"]["orders"]
    docs = list(col.find().sort("created_at", -1).limit(limit))
    for d in docs:
        d.pop("_id", None)
    return docs

@router.delete("/orders/{order_id}")
def delete_order(order_id: str):
    col = client["supply"]["orders"]
    res = col.delete_one({"order_id": order_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"status": "deleted"}
