from datetime import datetime
import os, csv

from app.interfaces.core.metrics_logger import MetricsLogger
from app.services.core.quality_monitor import CSVQualityMonitor

METRICS_FILE = "app/logs/metrics.csv"

class CSVLoggerService(MetricsLogger):
    def log_response(self, **kwargs) -> None:
        os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
        monitor = CSVQualityMonitor()

        with open(METRICS_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.utcnow().isoformat(),
                kwargs.get("restaurant_id", ""),
                kwargs.get("user_id", ""),
                kwargs.get("agent_type", ""),
                kwargs.get("prompt_version", ""),
                kwargs.get("model", ""),
                len(kwargs.get("prompt", "")),
                len(kwargs.get("response", "")),
                kwargs.get("token_usage", 0),
                kwargs.get("latency_ms", 0),
                int(kwargs.get("is_bad_response", False))
            ])

        if monitor.check_quality_threshold(threshold=10):
            print("🔴 Kalite eşiği aşıldı.")
