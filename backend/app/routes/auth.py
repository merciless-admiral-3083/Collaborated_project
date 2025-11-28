from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

# JWT settings
SECRET_KEY = "5f8a39d5a4e8b377feac9e78cdf44f59e1b3466e024b3f1886413ffe7d9a8e1d"     
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Use PBKDF2-SHA256 instead of bcrypt to avoid compatibility issues
hasher = pbkdf2_sha256

# Temporary in-memory DB
users_db = {}

class RegisterModel(BaseModel):
    name: str
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register(user: RegisterModel):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password using PBKDF2-SHA256 (compatible with passlib)
    hashed_pw = hasher.hash(user.password)

    users_db[user.email] = {
        "name": user.name,
        "email": user.email,
        "password": hashed_pw
    }

    return {"message": "Registration successful"}


@router.post("/login")
def login(user: LoginModel):
    if user.email not in users_db:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    db_user = users_db[user.email]

    # Verify using PBKDF2-SHA256
    if not hasher.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}
