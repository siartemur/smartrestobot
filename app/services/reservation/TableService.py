from sqlalchemy.orm import Session
from datetime import date, time
from typing import List
from app.database.models import Table, Reservation, ReservationStatus
from app.database.schemas import TableStatusOut

class TableServiceImpl:
    def __init__(self, db: Session):
        self.db = db

    def get_all_tables(self, restaurant_id: int) -> List[Table]:
        return self.db.query(Table).filter(
            Table.restaurant_id == restaurant_id,
            Table.is_active == True
        ).all()

    def get_table(self, table_id: int) -> Table:
        return self.db.query(Table).filter(Table.id == table_id).first()

    def get_available_tables(self, restaurant_id: int, res_date: date, res_time: time, guest_count: int) -> List[Table]:
        # Tüm aktif masaları al
        all_tables = self.get_all_tables(restaurant_id)

        # Belirtilen tarih ve saatte rezerve edilen masaların ID’lerini al
        reserved_ids = {
            r.table_id for r in self.db.query(Reservation)
            .join(Table, Reservation.table_id == Table.id)
            .filter(
                Table.restaurant_id == restaurant_id,
                Reservation.date == res_date,
                Reservation.time == res_time,
                Reservation.status == ReservationStatus.confirmed
            ).all()
        }

        # Uygun ve yeterli kapasiteye sahip masaları döndür
        return [
            t for t in all_tables
            if t.id not in reserved_ids and t.capacity >= guest_count
        ]

    def create_table(self, table_data) -> Table:
        new_table = Table(
            table_code=table_data.table_code,
            capacity=table_data.capacity,
            location=table_data.location,
            restaurant_id=table_data.restaurant_id,
            is_active=True
        )
        self.db.add(new_table)
        self.db.commit()
        self.db.refresh(new_table)
        return new_table

    def deactivate_table(self, table_id: int) -> bool:
        table = self.get_table(table_id)
        if table:
            table.is_active = False
            self.db.commit()
            return True
        return False

    def activate_table(self, table_id: int) -> bool:
        table = self.get_table(table_id)
        if table:
            table.is_active = True
            self.db.commit()
            return True
        return False

    def get_table_status_by_restaurant(self, restaurant_id: int, date_: date, time_: time) -> List[TableStatusOut]:
        tables = self.get_all_tables(restaurant_id)

        reserved_table_ids = {
            r.table_id for r in self.db.query(Reservation)
            .join(Table)
            .filter(
                Table.restaurant_id == restaurant_id,
                Reservation.date == date_,
                Reservation.time == time_,
                Reservation.status == ReservationStatus.confirmed
            ).all()
        }

        return [
            TableStatusOut(
                restaurant_id=restaurant_id,
                restaurant_name="Dubliner",  # İsteğe bağlı dinamik yapılabilir
                table_id=table.id,
                table_code=table.table_code,
                capacity=table.capacity,
                location=table.location,
                is_reserved=table.id in reserved_table_ids
            )
            for table in tables
        ]
