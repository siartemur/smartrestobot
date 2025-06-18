from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, time
from app.services.reservation.ReservationService import ReservationServiceImpl
from app.services.reservation.TableService import TableServiceImpl
from app.database.db import get_db
from app.database.schemas import ReservationCreate, ReservationOut, TableOut

router = APIRouter(prefix="/api/reservations", tags=["Reservations"])


@router.post("/", response_model=ReservationOut)
def create_reservation(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db)
):
    service = ReservationServiceImpl(db)

    reservation = service.create_reservation(
        user_name=reservation_data.user_name,
        phone=reservation_data.phone,
        email=reservation_data.email,
        date=reservation_data.date,
        time=reservation_data.time,
        guest_count=reservation_data.guest_count,
        table_id=reservation_data.table_id,
        source=reservation_data.source,
        notes=reservation_data.notes or ""
    )
    return reservation



@router.get("/available", response_model=List[TableOut])
def get_available_tables(
    restaurant_id: int,
    date: date,
    time: time,
    guest_count: int,
    db: Session = Depends(get_db)
):
    service = TableServiceImpl(db)
    tables = service.get_available_tables(restaurant_id, date, time, guest_count)
    return tables
