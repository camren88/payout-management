from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models

from app.database import get_db
from app.services.payout_service import process_advance_payout

router = APIRouter()

@router.post("/advance/{sale_id}")
def advance_payout(
    sale_id: int,
    db: Session = Depends(get_db)
):
    return process_advance_payout(db, sale_id)

@router.get("/")
def get_payouts(db: Session = Depends(get_db)):
    return db.query(models.Payout).all()