import json
from datetime import datetime, date, time
from typing import List
from sqlalchemy.orm import Session
from app.interfaces.reservation.ReservationService import ReservationService
from app.database.models import Reservation
from app.database.schemas import ReservationCreate, ReservationOut

class ReservationServiceImpl(ReservationService):
    def __init__(self, db: Session):
        self.db = db

    def create_reservation(self, user_name, phone, email, date, time, guest_count, table_id, source, notes=None) -> Reservation:
        # ✅ Basit validation (isteğe bağlı geliştirilebilir)
        if not all([date, time, guest_count, table_id]):
            raise ValueError("Eksik rezervasyon bilgisi. Tarih, saat, kişi sayısı ve masa bilgisi zorunludur.")

        reservation = Reservation(
            user_name=user_name or "Guest",
            phone=phone or "",
            email=email or "",
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

        # ✅ Dinamik bilgi güncellemesi
        try:
            path = "restaurants/dubliner/dynamic_info.json"  # Çok kiracılı sistemde dinamik yapılabilir
            with open(path, "w") as f:
                json.dump({
                    "last_reserved_table": table_id,
                    "last_reserved_date": str(date),
                    "last_reserved_time": str(time),
                    "timestamp": datetime.utcnow().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"⚠️ dynamic_info.json güncellenemedi: {e}")

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
