# app/api/reservation.py

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class ReservationRequest(BaseModel):
    user_id: int
    restaurant_id: str
    date: str  # ISO format expected
    time: str
    people: int

@router.post("/reservation")
def create_reservation(reservation: ReservationRequest):
    # 🧪 Dummy cevap: gerçek sistemde DB kaydı gerekir
    return {
        "status": "success",
        "message": f"{reservation.people} kişilik rezervasyon alındı",
        "data": {
            "restaurant_id": reservation.restaurant_id,
            "datetime": f"{reservation.date} {reservation.time}",
            "user_id": reservation.user_id
        }
    }
