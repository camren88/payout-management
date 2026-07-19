from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models

from app.database import get_db
from app.schemas import WithdrawalCreate
from app.services.withdrawal_service import (withdraw_money, retry_withdrawal, handle_failed_withdrawal)

router = APIRouter()


@router.post("/")
def create_withdrawal(
    withdrawal: WithdrawalCreate,
    db: Session = Depends(get_db)
):
    return withdraw_money(
        db,
        withdrawal.user_id,
        withdrawal.amount
    )

@router.post("/retry/{withdrawal_id}")
def retry(
    withdrawal_id: int,
    db: Session = Depends(get_db)
):
    return retry_withdrawal(
        db,
        withdrawal_id
    )


@router.get("/")
def get_withdrawals(db: Session = Depends(get_db)):
    return db.query(models.Withdrawal).all()


@router.get("/{withdrawal_id}")
def get_withdrawal(withdrawal_id: int,
                   db: Session = Depends(get_db)):

    withdrawal = db.query(models.Withdrawal).filter(
        models.Withdrawal.id == withdrawal_id
    ).first()

    if not withdrawal:
        return {"error": "Withdrawal not found"}

    return withdrawal


@router.put("/{withdrawal_id}/status")
def update_withdrawal_status(
    withdrawal_id: int, 
    status: str, 
    db: Session = Depends(get_db)
):
    result = handle_failed_withdrawal(db, withdrawal_id, status)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result