# config.py

import os
import json
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Ortam ayarları
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Uygulama ayarları
APP_NAME = "SmartRestoBot"
VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./smartrestobot.db")

# JWT Ayarları (aktif edilmedi ama burada hazır)
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Stripe
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")

# SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")

# Diğer
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

# Prompt yapılandırması (JSON yerine config'ten)
PROMPT_VERSIONS = {
    "menu_v1": "Kullanıcı menü hakkında bilgi almak istiyor: {message}",
    "reservation_v1": "Kullanıcı rezervasyon talebinde bulunuyor: {message}",
    "general_v1": "Genel bilgi isteyen kullanıcı mesajı: {message}",
    "fallback_v1": "Yanıt verilemeyen kullanıcı mesajı: {message}\nKibarca yeniden ifade etmesini iste."
}
