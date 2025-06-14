# ✅ services/auth/jwt_auth_provider.py
import os
import jwt
from datetime import datetime, timedelta
from app.interfaces.auth.auth_provider import AuthProvider

JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))

# Dummy in-memory user db for prototyping only
USERS_DB = {}

class JWTAuthProvider(AuthProvider):
    def register(self, name: str, email: str, password: str) -> str:
        if email in USERS_DB:
            raise ValueError("Bu e-posta zaten kayıtlı.")
        USERS_DB[email] = {"name": name, "email": email, "password": password}
        return self._generate_token(email)

    def login(self, email: str, password: str) -> str:
        user = USERS_DB.get(email)
        if not user or user["password"] != password:
            raise ValueError("Geçersiz giriş.")
        return self._generate_token(email)

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.PyJWTError:
            raise ValueError("Geçersiz veya süre dolmuş token.")

    def _generate_token(self, email: str) -> str:
        payload = {
            "sub": email,
            "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)