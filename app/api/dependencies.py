from fastapi import Depends, HTTPException, status
from app.adapters.jwt_auth import get_current_user
from app.database import models

def get_admin_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
