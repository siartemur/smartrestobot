from typing import Dict, List
from app.interfaces.core.memory_manager import MemoryManager

class InMemoryMemoryManager(MemoryManager):
    def __init__(self):
        self._conversation_history: Dict[int, List[dict]] = {}
        self._context_memory: Dict[str, dict] = {}  # user_id + restaurant → context

    # 🔁 Mesaj geçmişi işlemleri
    def add_message(self, user_id: int, role: str, content: str) -> None:
        if user_id not in self._conversation_history:
            self._conversation_history[user_id] = []
        self._conversation_history[user_id].append({
            "role": role,
            "content": content
        })

    def get_history(self, user_id: int) -> List[dict]:
        return self._conversation_history.get(user_id, [])

    def reset_history(self, user_id: int) -> None:
        self._conversation_history[user_id] = []

    def clear_all(self) -> None:
        self._conversation_history.clear()
        self._context_memory.clear()

    # 🧠 Konuşma bağlamı işlemleri
    def _make_key(self, user_id: int, restaurant: str) -> str:
        return f"{user_id}:{restaurant}"

    def get_context(self, user_id: int, restaurant: str) -> dict:
        return self._context_memory.get(self._make_key(user_id, restaurant), {})

    def update_context(self, user_id: int, restaurant: str, new_data: dict) -> None:
        key = self._make_key(user_id, restaurant)
        current = self._context_memory.get(key, {})
        current.update(new_data)
        self._context_memory[key] = current

    def reset_context(self, user_id: int, restaurant: str) -> None:
        self._context_memory.pop(self._make_key(user_id, restaurant), None)
