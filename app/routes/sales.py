from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models,schemas

router = APIRouter()

@router.get("/")
def test():
    return {"message":"Sales Route Working"}

@router.post("/", response_model=schemas.SaleResponse)
def create_sale(
    sale: schemas.SaleCreate,
    db: Session = Depends(get_db)
):
    new_sale = models.Sale(
      user_id=sale.user_id,
      brand=sale.brand,
      earning=sale.earning
)

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale