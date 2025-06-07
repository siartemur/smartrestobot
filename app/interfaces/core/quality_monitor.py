from typing import Protocol

class QualityMonitor(Protocol):
    def check_quality_threshold(self, threshold: int = 10) -> bool:
        ...

    def classify_bad_response(self, response: str) -> str | None:
        ...

    def log_bad_response(self, restaurant_id: str, prompt: str, response: str, reason: str) -> None:
        ...
