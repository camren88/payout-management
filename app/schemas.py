from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    id: int
    username: str
    withdrawable_balance: float

    class Config:
        from_attributes = True #orm_mode = True