from typing import Protocol

class AuditLogger(Protocol):
    def log_interaction(self, user_id: int, message: str, response: str, agent_type: str) -> None:
        ...
