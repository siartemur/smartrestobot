from typing import Dict, List
from app.interfaces.core.memory_manager import MemoryManager

class InMemoryMemoryManager(MemoryManager):
    def __init__(self):
        self._conversation_history: Dict[int, List[dict]] = {}

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
