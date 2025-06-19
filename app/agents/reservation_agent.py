import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.agents.chains.reservation_chain import get_reservation_chain
from app.retriever.restaurant_data_loader import get_full_restaurant_context
from app.interfaces.core.memory_manager import MemoryManager
from app.core.usecases.make_reservation import try_make_reservation

class ReservationAgent:
    def __init__(self, memory_manager: MemoryManager, db_session: Session):
        self.chain = get_reservation_chain()
        self.memory = memory_manager
        self.db = db_session
        self.prompt_version = "v1.1"

    async def run(
        self,
        message: str,
        user_context: dict,
        restaurant: str = "dubliner",
        chat_history: list[dict] = None
    ) -> dict:
        user_id = user_context.get("user_id")

        # 1. Geçmiş mesajları hazırla
        history = chat_history if chat_history is not None else self.memory.get_history(user_id)
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

        # 2. Restoran bilgilerini al
        context = get_full_restaurant_context(restaurant)

        # 3. Kullanıcı bilgilerini temizle
        filtered_context = {k: v for k, v in user_context.items() if v not in (None, "")}

        # 4. Prompt girdisi hazırla
        prompt_input = {
            "message": message,
            "chat_history": history_text,
            "static_info": context.get("static_info", ""),
            "dynamic_info": json.dumps(context.get("dynamic_info", {})),
            "user_context": json.dumps(filtered_context, ensure_ascii=False),
            "current_date": datetime.utcnow().strftime("%Y-%m-%d")
        }

        # 5. LLM'den cevap al
        response = await self.chain.ainvoke(prompt_input)

        try:
            output = json.loads(response.content.strip())
        except Exception:
            output = {
                "reply": response.content.strip(),
                "reservation_details": None
            }

        reply = output.get("reply", "")
        reservation_data = output.get("reservation_details")

        # 6. Gerekli bilgiler tam mı kontrol et (rezervasyon yapma koşulu)
        if (
            isinstance(reservation_data, dict) and
            reservation_data.get("date") and
            reservation_data.get("time") and
            reservation_data.get("guest_count")
        ):
            try:
                reservation, info_text = try_make_reservation(
                    self.db, user_context, reservation_data
                )
                reply += f"\n\n{info_text}"
            except Exception as e:
                reply += f"\n\n⚠️ Rezervasyon sırasında bir hata oluştu: {e}"

        # 7. Hafızaya mesajları ekle
        self.memory.add_message(user_id, "user", message)
        self.memory.add_message(user_id, "assistant", reply)

        return {
            "reply": reply,
            "reservation_details": reservation_data,
            "meta": {
                "agent": "reservation",
                "version": self.prompt_version
            }
        }
