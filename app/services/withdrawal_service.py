from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import models

def withdraw_money(
        db: Session, user_id: int, amount: float
        ):
    user = db.query(models.User).filter(
    models.User.id == user_id
    ).first()

    if not user:
       return {"error": "User not found"}
    
    if user.withdrawable_balance < amount:
       return {"error": "Insufficient balance"}
    
    if (
    user.last_withdrawal_time
    and datetime.now() - user.last_withdrawal_time < timedelta(hours=24)
    ):
       return {
        "error": "Only one withdrawal is allowed every 24 hours."
      }
    user.withdrawable_balance -= amount
    user.last_withdrawal_time = datetime.now()

    withdrawal = models.Withdrawal(
    user_id=user.id,
    amount=amount,
    status="completed"
    )

    db.add(withdrawal)
    db.commit()
    db.refresh(withdrawal)

    return {
    "message": "Withdrawal successful",
    "withdrawal_id": withdrawal.id,
    "remaining_balance": user.withdrawable_balance
}


def retry_withdrawal(db: Session, withdrawal_id: int):

    withdrawal = db.query(models.Withdrawal).filter(
        models.Withdrawal.id == withdrawal_id
    ).first()

    if not withdrawal:
        return {"error": "Withdrawal not found"}

    if withdrawal.status != "failed":
        return {
            "error": "Only failed withdrawals can be retried"
        }

    withdrawal.status = "completed"

    db.commit()
    db.refresh(withdrawal)

    return {
        "message": "Withdrawal retried successfully",
        "withdrawal": withdrawal.id
    }


from datetime import datetime, timedelta

def create_withdrawal(db: Session, user_id: int, amount: float):
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    
    if user.withdrawable_balance < amount:
        return {"error": "Insufficient withdrawable balance"}

    # 3. --- BUSINESS RULE: 24-Hour Restriction ---
    # Find the user's most recent withdrawal (assuming you have a Withdrawal or Payout table tracking this)
    # Adjust 'models.Withdrawal' to match your actual database model name!
    last_withdrawal = db.query(models.Withdrawal).filter(
        models.Withdrawal.user_id == user_id
    ).order_by(models.Withdrawal.created_at.desc()).first()

    if last_withdrawal:
        
        time_since_last = datetime.utcnow() - last_withdrawal.created_at
        
        if time_since_last < timedelta(hours=24):
            # Calculate how many hours are left to show a helpful error message
            hours_left = 24 - (time_since_last.total_seconds() / 3600)
            return {"error": f"You can only withdraw once every 24 hours. Please wait {hours_left:.1f} more hours."}

    # 4. Process the withdrawal
    user.withdrawable_balance -= amount
    
    new_withdrawal = models.Withdrawal(
        user_id=user_id,
        amount=amount,
        status="pending", # Or 'completed' depending on your flow
        created_at=datetime.utcnow()
    )
    
    db.add(new_withdrawal)
    db.commit()
    db.refresh(new_withdrawal)

    return {"message": "Withdrawal successful", "remaining_balance": user.withdrawable_balance}


def handle_failed_withdrawal(db: Session, withdrawal_id: int, new_status: str):
    # Ensure the status is one of the failure states from the assignment
    failure_statuses = ["cancelled", "rejected", "failed"]
    
    if new_status.lower() not in failure_statuses:
        return {"error": f"Status must be one of: {', '.join(failure_statuses)}"}

    # 1. Fetch the withdrawal record
    withdrawal = db.query(models.Withdrawal).filter(models.Withdrawal.id == withdrawal_id).first()
    
    if not withdrawal:
        return {"error": "Withdrawal not found"}

    # 2. Prevent Double Refunding (Crucial Edge Case Handling)
    if withdrawal.status in failure_statuses:
        return {"error": "This withdrawal has already been refunded"}
        
    if withdrawal.status != "pending":
         return {"error": f"Cannot modify a withdrawal that is currently '{withdrawal.status}'"}

    # 3. Fetch the user
    user = db.query(models.User).filter(models.User.id == withdrawal.user_id).first()
    
    if not user:
        return {"error": "User not found"}

    #  --- BUSINESS RULE: Credit back the balance ---
    user.withdrawable_balance += withdrawal.amount
    
    
    withdrawal.status = new_status.lower()
    
    # Save to database
    db.commit()
    db.refresh(user)
    db.refresh(withdrawal)

    return {
        "message": f"Withdrawal marked as {new_status}. ₹{withdrawal.amount} credited back to user.",
        "new_balance": user.withdrawable_balance
    }