from typing import Protocol

class Agent(Protocol):
    async def run(self, message: str, user_context: dict) -> str:
        ...
