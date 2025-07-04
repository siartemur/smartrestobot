# ✅ MemoryManager arayüzü
from typing import Protocol

class MemoryManager(Protocol):
    def add_message(self, user_id: int, role: str, content: str) -> None:
        ...

    def get_history(self, user_id: int) -> list[dict]:
        ...

    def reset_history(self, user_id: int) -> None:
        ...

    def clear_all(self) -> None:
        ...

    def get_context(self, user_id: int, restaurant: str) -> dict:
        ...

    def update_context(self, user_id: int, restaurant: str, new_data: dict) -> None:
        ...

    def reset_context(self, user_id: int, restaurant: str) -> None:
        ...
