from typing import Protocol

class Sanitizer(Protocol):
    def sanitize_input(self, user_input: str) -> str:
        ...
