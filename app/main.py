from fastapi import FastAPI

from app.database import Base,engine
from app import models

from app.routes import sales

from app.routes import users

from app.routes import payouts

from app.routes import withdrawals

from app.routes import reconciliation

from app.routes import dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Payout Management System API is running!"}

app.include_router(
    sales.router,
    prefix="/sales",
    tags=["Sales"]
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

app.include_router(
    payouts.router,
    prefix="/payouts",
    tags=["Payouts"]
)

app.include_router(
    withdrawals.router,
    prefix="/withdrawals",
    tags=["Withdrawals"]
)

app.include_router(
    reconciliation.router,
    prefix="/reconciliation",
    tags=["Reconciliation"]
)

app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)