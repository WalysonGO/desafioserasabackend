from datetime import date, datetime
from fastapi import Depends, HTTPException
from sqlalchemy import case, func, asc
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Debt
from app.schemas import DebtCreate, DebtResponse
from app.models.debt import DebtStatus
from math import ceil

def create_debt(debt: DebtCreate, db: Session = Depends(get_db), user: dict = None):
    debt_data = debt.dict()
    debt_data.pop('status', None)

    # Verifica se a data de vencimento é menor que a data atual
    if debt.status:
        status = debt.status
    elif debt.due_date < datetime.now().date():
        status = DebtStatus.ATRASADO.value
    else:
        status = DebtStatus.PENDENTE.value

    db_debt = Debt(**debt_data, status=status, user_id=user["id"])
    db.add(db_debt)
    db.commit()
    db.refresh(db_debt)

    return DebtResponse.from_orm(db_debt).dict()

def get_all_debts(db: Session = Depends(get_db), page: int = 1, per_page: int = 10, status: str = None, user: dict = None):  
    total_items = db.query(Debt).filter(Debt.user_id == user["id"]).count()  
    total_pages = ceil(total_items / per_page)  

    if page < 1 or (page > total_pages and total_items > 0):  
        return {  
            "page": page,  
            "per_page": per_page,  
            "data": [],  
            "total": total_items,  
            "current": page,  
            "prev": page - 1 if page > 1 else None,  
            "next": page + 1 if page < total_pages else None,  
        }  

    offset = (page - 1) * per_page  

    if not status:  
        debts = db.query(Debt).filter(Debt.user_id == user["id"]).order_by(  
            case(  
                (Debt.due_date < datetime.utcnow(), 0),  # Dívidas vencidas são as primeiras  
                else_=1  # Dívidas não vencidas  
            ),  
            asc(Debt.due_date),  
        ).offset(offset).limit(per_page).all()  
    elif status and status != "all":  
        debts = db.query(Debt).filter(Debt.user_id == user["id"]).filter(Debt.status == status).order_by(  
            case(  
                (Debt.due_date < datetime.utcnow(), 0),  # Dívidas vencidas são as primeiras  
                else_=1  
            ),  
            asc(Debt.due_date),  
        ).offset(offset).limit(per_page).all()  
    else:  
        debts = db.query(Debt).filter(Debt.user_id == user["id"]).filter(Debt.status == status).order_by(asc(Debt.due_date)).offset(offset).limit(per_page).all()  
    
    debt_responses = [DebtResponse.from_orm(debt) for debt in debts]  

    data_json = {  
        "page": page,  
        "per_page": per_page,  
        "data": [debt.dict() for debt in debt_responses],  
        "total": total_items,  
        "current": page,  
        "prev": page - 1 if page > 1 else None,  
        "next": page + 1 if page < total_pages else None,  
    }  

    return data_json

def update_status_to_paid(debt_id: str, db: Session = Depends(get_db), user: dict = None):
    db_debt = db.query(Debt).filter(Debt.id == debt_id).filter(Debt.user_id == user["id"]).first()

    if db_debt:
        db_debt.status = DebtStatus.PAGO.value
        db.commit()
        db.refresh(db_debt)
        
        return DebtResponse.from_orm(db_debt).dict()
    
    return None

def update_debt(debt_id: str, debt: DebtCreate, db: Session, user: dict = None):
    db_debt = db.query(Debt).filter(Debt.id == debt_id).filter(Debt.user_id == user["id"]).first()
    
    if db_debt:
        for key, value in debt.dict().items():
            if key == 'due_date':
                if isinstance(value, str):
                    try:
                        db_debt.due_date = datetime.strptime(value, '%d/%m/%Y').date()
                    except ValueError:
                        raise ValueError("Data deve estar no formato 'dd/mm/yyyy'")
                elif isinstance(value, date):
                    db_debt.due_date = value
                else:
                    raise TypeError("due_date deve ser uma string ou um objeto Date")
            else:
                setattr(db_debt, key, value)

        db.commit()
        db.refresh(db_debt)
        
        return DebtResponse.from_orm(db_debt).dict()
    
    return None

def delete_debt(debt_id: str, db: Session = Depends(get_db), user: dict = None):
    db_debt = db.query(Debt).filter(Debt.id == debt_id).filter(Debt.user_id == user["id"]).first()
    if db_debt:
        db.delete(db_debt)
        db.commit()

        return True
    elif not db_debt:
        return False
    return False

def get_financial_summary(db: Session = Depends(get_db), user: dict = None, date_from = None, date_to = None):
    try:  
        date_from = datetime.strptime(date_from, '%d/%m/%Y') if date_from else None  
        date_to = datetime.strptime(date_to, '%d/%m/%Y') if date_to else None  
    except ValueError as e:  
        raise HTTPException(status_code=400, detail="O formato da data é inválido. Use o formato DD/MM/YYYY.") from e  
    
    if date_from and date_to:
        total_debts = db.query(Debt).filter(Debt.due_date.between(date_from, date_to)).filter(Debt.user_id == user["id"])
        total_pending = db.query(Debt).filter(Debt.due_date.between(date_from, date_to)).filter(Debt.status == DebtStatus.PENDENTE.value).filter(Debt.user_id == user["id"])
        total_paid = db.query(Debt).filter(Debt.due_date.between(date_from, date_to)).filter(Debt.status == DebtStatus.PAGO.value).filter(Debt.user_id == user["id"])
        total_overdue = db.query(Debt).filter(Debt.due_date.between(date_from, date_to)).filter(Debt.status == DebtStatus.ATRASADO.value).filter(Debt.user_id == user["id"])
    if date_from and not date_to:
        total_debts = db.query(Debt).filter(Debt.due_date >= date_from).filter(Debt.user_id == user["id"])
        total_pending = db.query(Debt).filter(Debt.due_date >= date_from).filter(Debt.status == DebtStatus.PENDENTE.value).filter(Debt.user_id == user["id"])
        total_paid = db.query(Debt).filter(Debt.due_date >= date_from).filter(Debt.status == DebtStatus.PAGO.value).filter(Debt.user_id == user["id"])
        total_overdue = db.query(Debt).filter(Debt.due_date >= date_from).filter(Debt.status == DebtStatus.ATRASADO.value).filter(Debt.user_id == user["id"])
    if not date_from and date_to:
        total_debts = db.query(Debt).filter(Debt.due_date <= date_to).filter(Debt.user_id == user["id"])
        total_pending = db.query(Debt).filter(Debt.due_date <= date_to).filter(Debt.status == DebtStatus.PENDENTE.value).filter(Debt.user_id == user["id"])
        total_paid = db.query(Debt).filter(Debt.due_date <= date_to).filter(Debt.status == DebtStatus.PAGO.value).filter(Debt.user_id == user["id"])
        total_overdue = db.query(Debt).filter(Debt.due_date <= date_to).filter(Debt.status == DebtStatus.ATRASADO.value).filter(Debt.user_id == user["id"])
    else:
        total_debts = db.query(Debt).filter(Debt.user_id == user["id"])
        total_pending = db.query(Debt).filter(Debt.status == DebtStatus.PENDENTE.value).filter(Debt.user_id == user["id"])
        total_paid = db.query(Debt).filter(Debt.status == DebtStatus.PAGO.value).filter(Debt.user_id == user["id"])
        total_overdue = db.query(Debt).filter(Debt.status == DebtStatus.ATRASADO.value).filter(Debt.user_id == user["id"])

    total_debt_value = db.query(func.sum(Debt.amount)).filter(Debt.user_id == user["id"]).scalar() or 0
    total_pending_value = db.query(func.sum(Debt.amount)).filter(Debt.status == DebtStatus.PENDENTE.value, Debt.user_id == user["id"]).scalar() or 0
    total_paid_value = db.query(func.sum(Debt.amount)).filter(Debt.status == DebtStatus.PAGO.value, Debt.user_id == user["id"]).scalar() or 0
    total_overdue_value = db.query(func.sum(Debt.amount)).filter(Debt.status == DebtStatus.ATRASADO.value, Debt.user_id == user["id"]).scalar() or 0
    average_debt_value = total_debt_value / total_debts.count() if total_debts.count() > 0 else 0
    percentage_paid = total_paid_value / total_debt_value if total_debt_value > 0 else 0
    percentage_pending = total_pending_value / total_debt_value if total_debt_value > 0 else 0
    percentage_overdue = total_overdue_value / total_debt_value if total_debt_value > 0 else 0

    data_json = {
        "total_debts": total_debts.count(),
        "total_overdue": total_overdue.count(),
        "total_pending": total_pending.count(),
        "total_paid": total_paid.count(),
        "percentage_paid": percentage_paid,
        "percentage_pending": percentage_pending,
        "percentage_overdue": percentage_overdue,
        "total_debt_value": total_debt_value,
        "total_pending_value": total_pending_value,
        "total_paid_value": total_paid_value,
        "total_overdue_value": total_overdue_value,
        "average_debt_value": average_debt_value
    }

    return data_json
