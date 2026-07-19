from sqlalchemy.orm import Session
from app import models


def reconcile_sale(db: Session, sale_id: int, status: str):

    sale = db.query(models.Sale).filter(
        models.Sale.id == sale_id
    ).first()

    if not sale:
        return {"error": "Sale not found"}

    user = db.query(models.User).filter(
        models.User.id == sale.user_id
    ).first()

    if not user:
        return {"error": "User not found"}

    if sale.status != "pending":
        return {"error": "Sale has already been reconciled"}

    # ---------------- APPROVED ---------------- #

    if status.lower() == "approved":

        sale.status = "approved"

        remaining_amount = sale.earning - sale.advance_amount

        user.withdrawable_balance += remaining_amount

        payout = models.Payout(
            user_id=user.id,
            sale_id=sale.id,
            payout_type="final",
            amount=remaining_amount,
            status="completed"
        )

        db.add(payout)

    # ---------------- REJECTED ---------------- #

    elif status.lower() == "rejected":

        sale.status = "rejected"

        if sale.advance_paid:

            user.withdrawable_balance -= sale.advance_amount

            if user.withdrawable_balance < 0:
                user.withdrawable_balance = 0 #Explanation of key design decisions and trade-offs

            payout = models.Payout(
                user_id=user.id,
                sale_id=sale.id,
                payout_type="adjustment",
                amount=-sale.advance_amount,
                status="completed"
            )

            db.add(payout)

    else:
        return {
            "error": "Status must be either approved or rejected"
        }

    db.commit()
    db.refresh(sale)
    db.refresh(user)

    return {
        "message": "Sale reconciled successfully",
        "sale_status": sale.status,
        "withdrawable_balance": user.withdrawable_balance
    }