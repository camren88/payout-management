from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter()


@router.get("/{user_id}")
def dashboard(user_id: int,
              db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        return {"error": "User not found"}

    total_sales = db.query(models.Sale).filter(
        models.Sale.user_id == user_id
    ).count()

    total_payouts = db.query(models.Payout).filter(
        models.Payout.user_id == user_id
    ).count()

    total_withdrawals = db.query(models.Withdrawal).filter(
        models.Withdrawal.user_id == user_id
    ).count()

    return {
        "user": user.username,
        "withdrawable_balance": user.withdrawable_balance,
        "total_sales": total_sales,
        "total_payouts": total_payouts,
        "total_withdrawals": total_withdrawals
    }