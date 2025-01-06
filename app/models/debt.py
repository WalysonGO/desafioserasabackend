import uuid
from sqlalchemy import Column, DateTime, Integer, String, Float, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from enum import Enum

class DebtStatus(str, Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    ATRASADO = "atrasado"

class Debt(Base):
    __tablename__ = "debts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String, default=DebtStatus.PENDENTE.value)
    observations = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="debts")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
