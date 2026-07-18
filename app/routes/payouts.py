from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.payout_service import process_advance_payout

router = APIRouter()

@router.post("/advance/{sale_id}")
def advance_payout(
    sale_id: int,
    db: Session = Depends(get_db)
):
    return process_advance_payout(db, sale_id)

    new_payout = models.Payout(
        user_id=user.id,
        sale_id=sale.id,
        payout_type="advance",
        amount=advance_amount,
        status="completed"
    )