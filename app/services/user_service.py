from datetime import datetime
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.models.debt import Debt
from app.schemas import UserCreate, UserLogin
from app.services.auth_service import hash_password, verify_password, create_token

def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully!"}

def authenticate_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user and verify_password(user.password, db_user.hashed_password):
        return create_token({"sub": db_user.email})
    return None

def update_overdue_debts(db: Session = Depends(get_db)):
    overdue_debts = db.query(Debt).filter(Debt.due_date < datetime.now(), Debt.status != 'pago').all()
    for debt in overdue_debts:
        debt.status = 'atrasado'
        db.commit()
    return None
