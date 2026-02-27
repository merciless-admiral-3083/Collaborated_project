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


from database.user_repository import create_user, get_user_by_email

@router.post("/register")
async def register(user: RegisterModel):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hasher.hash(user.password)

    user_data = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_pw
    }

    user_id = create_user(user_data)

    return {"message": "Registration successful", "user_id": user_id}


@router.post("/login")
async def login(user: LoginModel):
    db_user = get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not hasher.verify(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": str(db_user["_id"])})

    return {"access_token": token, "token_type": "bearer"}
