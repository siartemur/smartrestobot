from typing import List
from datetime import date, time
from sqlalchemy.orm import Session
from app.interfaces.reservation.ReservationService import ReservationService
from app.database.schemas import ReservationCreate, ReservationOut
from app.database.models import Reservation

class ReservationServiceImpl(ReservationService):
    def __init__(self, db: Session):
        self.db = db

    def create_reservation(self, user_name, phone, email, date, time, guest_count, table_id, source, notes=None) -> Reservation:
        reservation = Reservation(
            user_name=user_name,
            phone=phone,
            email=email,
            date=date,
            time=time,
            guest_count=guest_count,
            table_id=table_id,
            notes=notes,
            source=source,
            status="confirmed"
        )
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def get_reservations_for_day(self, date_: date) -> List[Reservation]:
        return self.db.query(Reservation).filter(Reservation.date == date_).all()

    def cancel_reservation(self, reservation_id: int) -> bool:
        reservation = self.db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if reservation:
            reservation.status = "cancelled"
            self.db.commit()
            return True
        return False
