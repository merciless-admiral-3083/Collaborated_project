# backend/app/routes/orders.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.db import db  # <-- using db directly from db.py

router = APIRouter()

# ---------------------------
# Pydantic Input Model
# ---------------------------
class OrderIn(BaseModel):
    order_id: str
    country: str
    supplier: str
    qty: int
    eta: str | None = None

# Reference to the collection
orders_collection = db["orders"]


# ---------------------------
# CREATE ORDER
# ---------------------------
@router.post("/orders")
def create_order(payload: OrderIn):
    # Check if already exists
    if orders_collection.find_one({"order_id": payload.order_id}):
        raise HTTPException(400, "Order ID already exists.")

    doc = payload.dict()
    doc["created_at"] = datetime.utcnow().isoformat()

    orders_collection.insert_one(doc)
    return {"status": "ok", "order_id": payload.order_id}


# ---------------------------
# GET SINGLE ORDER
# ---------------------------
@router.get("/orders/{order_id}")
def get_order(order_id: str):
    doc = orders_collection.find_one({"order_id": order_id})
    if not doc:
        raise HTTPException(404, "Order not found")

    doc.pop("_id", None)
    return doc


# ---------------------------
# LIST ORDERS
# ---------------------------
@router.get("/orders")
def list_orders(limit: int = 50):
    docs = list(orders_collection.find().sort("created_at", -1).limit(limit))

    for d in docs:
        d.pop("_id", None)

    return docs


# ---------------------------
# DELETE ORDER
# ---------------------------
@router.delete("/orders/{order_id}")
def delete_order(order_id: str):
    res = orders_collection.delete_one({"order_id": order_id})

    if res.deleted_count == 0:
        raise HTTPException(404, "Order not found")

    return {"status": "deleted"}
