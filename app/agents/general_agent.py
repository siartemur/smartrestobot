from app.agents.chains.general_chain import get_general_chain
from app.retriever.restaurant_data_loader import get_full_restaurant_context
from app.interfaces.core.memory_manager import MemoryManager

class GeneralAgent:
    def __init__(self, memory_manager: MemoryManager):
        self.chain = get_general_chain()
        self.memory = memory_manager

    async def run(self, message: str, user_context: dict, restaurant: str = "dubliner", chat_history: list[dict] = None) -> str:
        user_id = user_context.get("user_id")
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in (chat_history or [])])

        # Restoran bilgileri
        context = get_full_restaurant_context(restaurant)

        # Zincire gönderilecek prompt input
        prompt_input = {
            "message": message,
            "chat_history": history_text,
            "static_info": context.get("static_info", "")
        }

        # LLM yanıtı al
        response = await self.chain.ainvoke(prompt_input)
        reply = response.content.strip()

        # Hafızaya yaz
        if user_id:
            self.memory.add_message(user_id, "user", message)
            self.memory.add_message(user_id, "assistant", reply)

        return reply
