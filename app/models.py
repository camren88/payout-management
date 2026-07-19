from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    withdrawable_balance = Column(Float, default=0.0)
    last_withdrawal_time = Column(DateTime, nullable=True)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String, default="pending")

    earning = Column(Float, nullable=False)

    advance_paid = Column(Boolean, default=False)

    advance_amount = Column(Float, default=0.0)

    user = relationship("User")    

class Payout(Base):
    __tablename__ = "payouts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    sale_id = Column(Integer, ForeignKey("sales.id"))

    payout_type = Column(String, nullable=False)  # advance, final, adjustment

    amount = Column(Float, nullable=False)

    status = Column(String, default="pending")  # pending, success, failed

    user = relationship("User")

    sale = relationship("Sale")    

class Withdrawal(Base):
    __tablename__ = "withdrawals"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    amount = Column(Float, nullable=False)

    status = Column(String, default="completed")

    user = relationship("User")    