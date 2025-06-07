import jwt
import os
from datetime import datetime, timedelta
from app.interfaces.auth.auth_provider import AuthProvider

# Config ayarları (env üzerinden veya hardcoded olarak ayarlanabilir)
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60

# Basit kullanıcı veri yapısı
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
            decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded
        except jwt.PyJWTError:
            raise ValueError("Geçersiz veya süresi dolmuş token.")

    def _generate_token(self, email: str) -> str:
        payload = {
            "sub": email,
            "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
