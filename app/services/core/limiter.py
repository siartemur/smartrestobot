from collections import defaultdict
from datetime import datetime, timedelta
from app.interfaces.core.limiter import Limiter

class InMemoryLimiter(Limiter):
    def __init__(self, limit: int = 100, window_seconds: int = 3600):
        self._user_requests = defaultdict(list)
        self.limit = limit
        self.window_seconds = window_seconds

    def is_rate_limited(self, user_id: int) -> bool:
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)

        # Eski istekleri temizle
        self._user_requests[user_id] = [
            timestamp for timestamp in self._user_requests[user_id]
            if timestamp > window_start
        ]

        if len(self._user_requests[user_id]) >= self.limit:
            return True

        self._user_requests[user_id].append(now)
        return False
