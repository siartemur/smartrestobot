# ✅ app/agents/menu_agent.py

import json
from datetime import datetime
from app.agents.chains.menu_chain import get_menu_chain
from app.retriever.restaurant_data_loader import get_full_restaurant_context
from app.interfaces.core.memory_manager import MemoryManager

class MenuAgent:
    def __init__(self, memory_manager: MemoryManager):
        self.chain = get_menu_chain()
        self.memory = memory_manager
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
            "menu": context.get("menu", {}),
            "user_context": filtered_context,
            "current_date": datetime.utcnow().strftime("%Y-%m-%d")
        }

        # ✅ DEBUG LOG
        print("---- DEBUG: prompt_input ----")
        for key, val in prompt_input.items():
            print(f"{key}: {type(val)}")
        print("-----------------------------")

        # 5. LLM'den cevap al
        response = await self.chain.ainvoke(prompt_input)

        try:
            output = json.loads(response.content.strip())
        except Exception:
            output = {
                "reply": response.content.strip()
            }

        reply = output.get("reply", "")

        # 6. Hafızaya mesajları ekle
        self.memory.add_message(user_id, "user", message)
        self.memory.add_message(user_id, "assistant", reply)

        return {
            "reply": reply,
            "meta": {
                "agent": "menu",
                "version": self.prompt_version
            }
        }
