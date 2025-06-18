from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import os

from app.database import models
from app.database.db import get_db

# 👇 Memory Manager importu (yeni)
from app.services.core.memory_manager import InMemoryMemoryManager

# JWT ayarları
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# ✅ Auth
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ✅ Geçici admin
def get_admin_user():
    return models.User(
        id=1,
        name="Test Admin",
        email="admin@test.com",
        is_admin=True
    )

# ✅ Memory Manager — Singleton olarak sadece 1 kez oluşturulacak
memory_manager = InMemoryMemoryManager()

def get_memory_manager():
    return memory_manager
