import json
from sqlalchemy.orm import Session
from app.agents.chains.reservation_chain import get_reservation_chain
from app.retriever.restaurant_data_loader import get_full_restaurant_context
from app.interfaces.core.memory_manager import MemoryManager
from app.services.reservation.ReservationService import ReservationServiceImpl
from app.services.reservation.TableService import TableServiceImpl

class ReservationAgent:
    def __init__(self, memory_manager: MemoryManager, db_session: Session):
        self.chain = get_reservation_chain()
        self.memory = memory_manager
        self.db = db_session

    async def run(
        self,
        message: str,
        user_context: dict,
        restaurant: str = "dubliner",
        chat_history: list[dict] = None
    ) -> dict:
        user_id = user_context.get("user_id")

        # ✅ 1. Hafıza geçmişini hazırla
        history = chat_history if chat_history is not None else self.memory.get_history(user_id)
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

        # ✅ 2. Restoran bilgileri
        context = get_full_restaurant_context(restaurant)

        # ✅ 3. Prompt girişi oluştur
        prompt_input = {
            "message": message,
            "chat_history": history_text,
            "static_info": context.get("static_info", ""),
            "dynamic_info": json.dumps(context.get("dynamic_info", {})),
            "user_context": user_context
        }

        # ✅ 4. LLM cevabını al
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

        # ✅ 5. Eğer rezervasyon yapılabiliyorsa:
        if reservation_data:
            try:
                table_service = TableServiceImpl(self.db)
                available_tables = table_service.get_available_tables(
                    restaurant_id=1,  # Eğer çok kiracılı yapıdaysan user_context["restaurant_id"] alınabilir
                    res_date=reservation_data["date"],
                    res_time=reservation_data["time"],
                    guest_count=reservation_data["guest_count"]
                )

                if not available_tables:
                    reply += "\n\n⚠️ Maalesef bu tarih ve saatte uygun masa bulunamadı."
                else:
                    selected_table = available_tables[0]

                    reservation_service = ReservationServiceImpl(self.db)
                    reservation_service.create_reservation(
                        user_name=user_context.get("name", "Guest"),
                        phone=user_context.get("phone", ""),
                        email=user_context.get("email", ""),
                        date=reservation_data["date"],
                        time=reservation_data["time"],
                        guest_count=reservation_data["guest_count"],
                        table_id=selected_table.id,
                        source="chat"
                    )

                    reply += f"\n\n✅ Rezervasyon oluşturuldu: {selected_table.capacity} kişilik masa ({selected_table.table_code})."
            except Exception as e:
                reply += f"\n\n⚠️ Rezervasyon sırasında bir hata oluştu: {e}"

        # ✅ 6. Hafızaya ekle
        self.memory.add_message(user_id, "user", message)
        self.memory.add_message(user_id, "assistant", reply)

        return {
            "reply": reply,
            "reservation_details": reservation_data
        }
