from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, time, datetime
from enum import Enum

# ✅ Kullanıcı Şemaları
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool

    model_config = {
        "from_attributes": True
    }

# ✅ Enum'lar
class ReservationSource(str, Enum):
    chat = "chat"
    web = "web"
    phone = "phone"
    walk_in = "walk_in"

class ReservationStatus(str, Enum):
    confirmed = "confirmed"
    cancelled = "cancelled"
    expired = "expired"

# ✅ Table Şemaları
class TableBase(BaseModel):
    table_code: str
    capacity: int
    location: Optional[str] = None
    is_active: Optional[bool] = True

class TableCreate(TableBase):
    restaurant_id: int

class TableOut(TableBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# ✅ Reservation Şemaları
class ReservationBase(BaseModel):
    date: date
    time: time
    guest_count: int
    table_id: int
    user_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    notes: Optional[str] = None
    source: Optional[ReservationSource] = ReservationSource.chat
    status: Optional[ReservationStatus] = ReservationStatus.confirmed

class ReservationCreate(ReservationBase):
    pass

class ReservationOut(ReservationBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class TableStatusOut(BaseModel):
    restaurant_id: int
    restaurant_name: str
    table_id: int
    table_code: str
    capacity: int
    location: Optional[str]
    is_reserved: bool

    class Config:
        orm_mode = True
