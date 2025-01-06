from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum
import uuid
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DebtCreate(BaseModel):
    title: str
    amount: float
    due_date: date | str
    status: str | None = "pendente"
    observations: Optional[str] = None

class DebtStatus(str, Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    ATRASADO = "atrasado"

class DebtBase(BaseModel):
    title: str
    amount: float
    due_date: date
    status: DebtStatus
    observations: Optional[str] = None

class DebtResponse(DebtBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
