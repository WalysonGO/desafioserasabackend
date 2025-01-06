import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas import UserCreate, UserLogin, UserResponse
from app.services.auth_service import get_current_user
from app.services.user_service import create_user, authenticate_user
from app.database import get_db

user_router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

@user_router.post("/register", response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return create_user(user, db)

@user_router.post("/login", response_model=dict)
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(user, db)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@user_router.get("/me", response_model=UserResponse)
def read_users_me(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == current_user['email']).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

