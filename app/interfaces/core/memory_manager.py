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
