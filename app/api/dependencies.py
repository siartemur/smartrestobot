# ✅ app/api/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import os

from app.database import models
from app.database.db import get_db

SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

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



#def get_admin_user(current_user: models.User = Depends(get_current_user)):
#    if not current_user.is_admin:
#        raise HTTPException(
#            status_code=status.HTTP_403_FORBIDDEN,
#            detail="Admin privileges required"
#        )
#    return current_user



# ✅ app/api/dependencies.py içinde TEST için geçici get_admin_user
def get_admin_user():
    return models.User(
        id=1,
        name="Test Admin",
        email="admin@test.com",
        is_admin=True
        # ❌ password, created_at, updated_at gibi alanları geçme
    )
