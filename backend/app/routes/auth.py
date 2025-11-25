# backend/app/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db import client
from src.utils.auth import hash_password, verify_password, create_access_token, decode_token

router = APIRouter()

class RegisterIn(BaseModel):
    username: str
    password: str
    email: str | None = None

class LoginIn(BaseModel):
    username: str
    password: str

@router.post("/auth/register")
def register(payload: RegisterIn):
    col = client["users"]["users"]
    if col.find_one({"username": payload.username}):
        raise HTTPException(status_code=400, detail="username_exists")
    doc = {"username": payload.username, "password": hash_password(payload.password), "email": payload.email}
    col.insert_one(doc)
    return {"status": "created"}

@router.post("/auth/login")
def login(payload: LoginIn):
    col = client["users"]["users"]
    user = col.find_one({"username": payload.username})
    if not user:
        raise HTTPException(status_code=401, detail="invalid_credentials")
    if not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="invalid_credentials")
    token = create_access_token({"sub": payload.username})
    return {"access_token": token, "token_type": "bearer"}

# Example protected endpoint helper
from fastapi import Header
def get_current_user(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth header")
    payload = decode_token(parts[1])
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload.get("sub")
