# from typing import List, Optional
# from pydantic import BaseModel


# class Table(BaseModel):
#     id: int
#     table_code: str
#     capacity: int
#     location: Optional[str]
#     is_active: bool = True


# class Restaurant(BaseModel):
#     id: int
#     name: str
#     address: Optional[str]
#     phone: Optional[str]
#     open_hours: Optional[str]
#     tables: List[Table] = []

#     def get_available_tables(self, guest_count: int) -> List[Table]:
#         return [table for table in self.tables if table.capacity >= guest_count and table.is_active]
