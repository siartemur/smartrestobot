# app/interfaces/core/metrics_logger.py

from abc import ABC, abstractmethod

class MetricsLogger(ABC):
    @abstractmethod
    def log_response(self, **kwargs) -> None:
        pass
