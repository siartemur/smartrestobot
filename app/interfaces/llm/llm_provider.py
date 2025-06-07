from typing import Protocol

class LLMProvider(Protocol):
    def generate(self, prompt: str, context: dict = {}) -> str:
        ...
