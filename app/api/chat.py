import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, Dict

from app.database.models import ChatHistory
from app.database.db import get_db
from app.database import models
from app.services.core.quality_monitor import CSVQualityMonitor
from app.services.core.logger_service import log_response_metrics
from app.agents.reservation_agent import ReservationAgent
from app.agents.general_agent import GeneralAgent
from app.services.core.memory_manager import InMemoryMemoryManager  # ✅ Memory servisi

# ✅ .env yükle
load_dotenv()
router = APIRouter()
memory = InMemoryMemoryManager()  # ✅ memory nesnesi

# ✅ Giriş-çıkış modelleri
class ChatRequest(BaseModel):
    message: str
    restaurant: Optional[str] = "dubliner"
    user_context: Optional[Dict] = {}

class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat: ChatRequest, db: Session = Depends(get_db)):
    try:
        user_id = chat.user_context.get("user_id", 0)

        # ✅ 1. Mesajı geçmişe ekle (USER)
        memory.add_message(user_id, "user", chat.message)

        # ✅ 2. Agent seçimi
        message_lower = chat.message.lower()
        if any(keyword in message_lower for keyword in ["rezervasyon", "ayır", "masa", "kişilik"]):
            agent = ReservationAgent(memory_manager=memory, db_session=db)
            agent_type = "reservation"
        else:
            agent = GeneralAgent(memory_manager=memory)
            agent_type = "general"

        # ✅ 3. Geçmiş konuşma alınır
        history = memory.get_history(user_id)

        # ✅ 4. Yanıtı üret (JSON formatında gelir)
        result = await agent.run(
            message=chat.message,
            user_context=chat.user_context,
            restaurant=chat.restaurant,
            chat_history=history
        )

        reply = result.get("reply", "Bir hata oluştu.")
        memory.add_message(user_id, "assistant", reply)

        # ✅ 5. Kötü yanıt kontrolü
        monitor = CSVQualityMonitor()
        reason = monitor.classify_bad_response(reply)
        is_bad = reason is not None

        # ✅ 6. DB kaydı
        chat_record = models.ChatHistory(
            user_id=user_id,
            message=chat.message,
            response=reply,
            prompt_version="v2",
            agent_type=agent_type
        )
        db.add(chat_record)
        db.commit()

        # ✅ 7. Metrik logla
        log_response_metrics(
            restaurant_id=chat.restaurant,
            user_id=user_id,
            prompt=chat.message,
            response=reply,
            model="gpt-4",
            agent_type=agent_type,
            prompt_version="v2",
            token_usage=len(reply.split()),
            latency_ms=150,
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
