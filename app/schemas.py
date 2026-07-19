from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    withdrawable_balance: float

    class Config:
        from_attributes = True #orm_mode = True

class SaleCreate(BaseModel):
    user_id: int
    brand: str
    earning: float        

class SaleResponse(BaseModel):
    id: int
    user_id: int
    brand: str
    earning: float
    status: str
    advance_paid: bool
    advance_amount: float

    class Config:
        from_attributes = True    

class WithdrawalCreate(BaseModel):
    user_id: int
    amount: float        