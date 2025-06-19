from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date, time
from app.database.schemas import TableCreate, TableOut, TableAvailabilityOut, TableStatusOut

class TableService(ABC):

    @abstractmethod
    def create_table(self, table_data: TableCreate) -> TableOut:
        pass

    @abstractmethod
    def get_all_tables(self, restaurant_id: int) -> List[TableOut]:
        pass

    @abstractmethod
    def get_available_tables(
        self,
        restaurant_id: int,
        date_: date,
        time_: time,
        guest_count: int,
        preferred_location: Optional[str] = None  # ✅ YENİ parametre eklendi
    ) -> List[TableAvailabilityOut]:
        pass

    @abstractmethod
    def deactivate_table(self, table_id: int) -> bool:
        pass

    @abstractmethod
    def activate_table(self, table_id: int) -> bool:
        pass

    @abstractmethod
    def get_table(self, table_id: int) -> Optional[TableOut]:
        pass

    @abstractmethod
    def get_table_status_by_restaurant(
        self, restaurant_id: int, date_: date, time_: time
    ) -> List[TableStatusOut]:
        pass
