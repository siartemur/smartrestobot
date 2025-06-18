from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Date, Time, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# ✅ ENUM'lar
class ReservationSource(str, enum.Enum):
    chat = "chat"
    web = "web"
    phone = "phone"
    walk_in = "walk_in"

class ReservationStatus(str, enum.Enum):
    confirmed = "confirmed"
    cancelled = "cancelled"
    expired = "expired"

# ✅ RESTAURANT MODELİ
class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="restaurant", cascade="all, delete-orphan")
    tables = relationship("Table", back_populates="restaurant", cascade="all, delete-orphan")

# ✅ KULLANICI MODELİ
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    restaurant = relationship("Restaurant", back_populates="users")
    chat_history = relationship("ChatHistory", back_populates="user")

# ✅ CHAT GEÇMİŞİ
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    prompt_version = Column(String, default="v1")
    agent_type = Column(String, default="general")

    user = relationship("User", back_populates="chat_history")

# ✅ MASA MODELİ
class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    table_code = Column(String, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    restaurant = relationship("Restaurant", back_populates="tables")
    reservations = relationship("Reservation", back_populates="table")

# ✅ REZERVASYON MODELİ
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    guest_count = Column(Integer, nullable=False)

    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    table = relationship("Table", back_populates="reservations")

    notes = Column(String, nullable=True)
    source = Column(Enum(ReservationSource), default=ReservationSource.chat)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.confirmed)
    email_reminder_sent = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
