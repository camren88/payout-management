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
      earning=sale.earning,
      status="pending"
)

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale

@router.get("/")
def get_sales(db: Session = Depends(get_db)):
    return db.query(models.Sale).all()


@router.get("/{sale_id}")
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(
        models.Sale.id == sale_id
    ).first()

    if not sale:
        return {"error": "Sale not found"}

    return sale