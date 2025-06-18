from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.services.reservation.TableService import TableServiceImpl
from app.database.db import get_db
from app.database.schemas import TableCreate, TableOut

router = APIRouter(prefix="/api/tables", tags=["Tables"])


@router.get("/", response_model=List[TableOut])
def get_tables(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    service = TableServiceImpl(db)
    return service.get_all_tables(restaurant_id)


@router.post("/", response_model=TableOut)
def create_table(
    table_data: TableCreate,
    db: Session = Depends(get_db)
):
    service = TableServiceImpl(db)
    return service.create_table(table_data)
