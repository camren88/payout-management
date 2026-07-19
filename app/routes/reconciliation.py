from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.reconciliation_service import reconcile_sale

router = APIRouter()


@router.post("/{sale_id}")
def reconcile(
    sale_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    return reconcile_sale(
        db,
        sale_id,
        status
    )