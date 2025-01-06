from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas import DebtCreate, DebtStatus
from app.services.debt_service import (
    create_debt, get_all_debts, update_debt, delete_debt, get_financial_summary, update_status_to_paid
)
from app.database import get_db
from app.services.auth_service import get_current_user

debt_router = APIRouter()

@debt_router.post("/", response_model=dict)
def add_debt(debt: DebtCreate, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_debt(debt, db, user=user)

@debt_router.get("/", response_model=dict)
def list_debts(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    status: str = Query(None),
    user: dict = Depends(get_current_user)
):
    """
    Lista todas as dívidas associadas ao usuário logado com paginação baseada em páginas.
    """
    if not status or status == "all":
        return get_all_debts(db, page=page, per_page=per_page, status=None, user=user)
    if DebtStatus(status) == DebtStatus.PENDENTE:
        return get_all_debts(db, page=page, per_page=per_page, status=DebtStatus.PENDENTE.value, user=user)
    elif DebtStatus(status) == DebtStatus.PAGO:
        return get_all_debts(db, page=page, per_page=per_page, status=DebtStatus.PAGO.value, user=user)
    elif DebtStatus(status) == DebtStatus.ATRASADO:
        return get_all_debts(db, page=page, per_page=per_page, status=DebtStatus.ATRASADO.value, user=user)
    
@debt_router.put("/{debt_id}", response_model=dict)
def edit_debt(debt_id: str, debt: DebtCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Edita uma dívida existente. Requer autenticação.
    """
    updated_debt = update_debt(debt_id, debt, db, user=user)
    if not updated_debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    return updated_debt

@debt_router.delete("/{debt_id}", response_model=dict)
def remove_debt(debt_id: str, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Remove uma dívida existente. Requer autenticação.
    """
    if not delete_debt(debt_id, db, user=user):
        raise HTTPException(status_code=404, detail="Debt not found")
    return {"message": "Debt deleted successfully"}

@debt_router.get("/summary", response_model=dict)
def financial_summary(db: Session = Depends(get_db), user: dict = Depends(get_current_user), date_from = None, date_to = None):
    """
    Fornece um resumo financeiro para o usuário logado.
    """

    return get_financial_summary(db, user=user, date_from=date_from, date_to=date_to)

# Rota para atualizar por ID, para alterar o status para pago
@debt_router.put("/update-status-to-payed/{debt_id}", response_model=dict)
def update_status_to_payed(debt_id: str, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    updated_debt = update_status_to_paid(debt_id, db, user=user)
    if not updated_debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    return updated_debt