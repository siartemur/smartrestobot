from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date, time
from app.database.models import Reservation, ReservationSource

class ReservationService(ABC):

    @abstractmethod
    def create_reservation(
        self,
        user_name: str,
        phone: Optional[str],
        email: Optional[str],
        date: date,
        time: time,
        guest_count: int,
        table_id: int,
        source: ReservationSource,
        notes: Optional[str] = None
    ) -> Reservation:
        pass

    @abstractmethod
    def get_reservations_for_day(self, date: date) -> List[Reservation]:
        pass

    @abstractmethod
    def cancel_reservation(self, reservation_id: int) -> bool:
        pass
