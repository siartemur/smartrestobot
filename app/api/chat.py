# app/api/chat.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.models import ChatHistory
from app.database.db import get_db
from app.database import models
from app.services.core.quality_monitor import CSVQualityMonitor
from app.services.core.logger_service import log_response_metrics


# ✅ .env yükle
load_dotenv()

# ✅ Router başlat
router = APIRouter()

# ✅ İstek/cevap modelleri
class ChatRequest(BaseModel):
    message: str
    user_id: int

class ChatResponse(BaseModel):
    response: str

# ✅ OpenAI istemcisi
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Sohbet endpoint
@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(chat: ChatRequest, db: Session = Depends(get_db)):
    try:
        # ✅ LLM cevabı üret
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sen restoran asistanısın, menü ve rezervasyonla ilgili yardımcı ol."},
                {"role": "user", "content": chat.message}
            ]
        )
        reply = response.choices[0].message.content

        # ✅ Kötü cevap kontrolü
        monitor = CSVQualityMonitor()
        reason = monitor.classify_bad_response(reply)
        is_bad = reason is not None

        # ✅ Cevabı DB'ye kaydet
        chat_record = models.ChatHistory(
            user_id=chat.user_id,
            message=chat.message,
            response=reply,
            prompt_version="v2",
            agent_type="menu"
        )
        db.add(chat_record)
        db.commit()

        # ✅ Metrik logla
        log_response_metrics(
            restaurant_id="rest_001",
            user_id=chat.user_id,
            prompt=chat.message,
            response=reply,
            model="gpt-4",
            agent_type="menu",
            prompt_version="v2",
            token_usage=len(reply.split()),
            latency_ms=150,  # örnek
            is_bad_response=is_bad
        )

        return {"response": reply}
    except Exception as e:
        return {"response": f"Hata: {str(e)}"}


@router.get("/chat/history")
def get_chat_history(db: Session = Depends(get_db)):
    history = db.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).limit(20).all()
    return [
        {
            "id": chat.id,
            "message": chat.message,
            "response": chat.response,
            "timestamp": chat.timestamp.isoformat()
        }
        for chat in history
    ]
