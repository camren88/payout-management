from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/")
def create_user():
    return {"message": "Coming Soon"}