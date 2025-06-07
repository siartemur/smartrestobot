from typing import Protocol

class MetricsReader(Protocol):
    def show_metrics_summary(self) -> None:
        ...
