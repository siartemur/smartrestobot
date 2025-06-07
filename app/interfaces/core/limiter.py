from typing import Protocol

class Limiter(Protocol):
    def is_rate_limited(self, user_id: int) -> bool:
        ...
