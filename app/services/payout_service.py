from sqlalchemy.orm import Session
from app import models

def process_advance_payout(db: Session, sale_id: int):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()

    if not sale:
       return {"error": "Sale not found"}
    
    if sale.status != "pending":
       return {"error": "Sale is not pending"}

    if sale.advance_paid:
       return {"error": "Advance already paid"}
    
    advance_amount = sale.earning * 0.10  

    sale.advance_amount = advance_amount
    sale.advance_paid = True

    user = db.query(models.User)

    user.withdrawable_balance += advance_amount

    new_payout = models.Payout(...)

    db.add(new_payout)
    db.commit()