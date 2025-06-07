import os, csv, re
import pandas as pd
from datetime import datetime, timedelta
from app.interfaces.core.quality_monitor import QualityMonitor
from app.services.notifications.slack_notifier import send_slack_alert


BAD_RESPONSES_CSV = "app/logs/bad_responses.csv"

class CSVQualityMonitor(QualityMonitor):
    def check_quality_threshold(self, threshold: int = 10) -> bool:
        if not os.path.exists(BAD_RESPONSES_CSV):
            return False
        try:
            df = pd.read_csv(BAD_RESPONSES_CSV)
            if df.empty:
                return False
            df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(None)
            recent_bad = df[df["timestamp"] > datetime.utcnow() - timedelta(hours=24)]
            if len(recent_bad) >= threshold:
                send_slack_alert(f"🚨 Kalite uyarısı: Son 24 saatte {len(recent_bad)} kötü yanıt üretildi.")
                return True
        except Exception:
            return False
        return False

    def classify_bad_response(self, response: str) -> str | None:
        response = response.strip().lower()
        if len(response) < 10:
            return "too_short"
        if "i don't know" in response or "i am just an ai" in response:
            return "generic"
        if "error" in response or "traceback" in response:
            return "error_output"
        if "weather" in response or "politics" in response:
            return "off_topic"
        if re.search(r"\b(\w+)\b\s+\1", response):
            return "repetition"
        if "özür dilerim" in response or "üzgünüm" in response:
            return "apology"
        if "yardımcı olamıyorum" in response or "emin değilim" in response:
            return "uncertain"
        return None

    def log_bad_response(self, restaurant_id: str, prompt: str, response: str, reason: str):
        os.makedirs(os.path.dirname(BAD_RESPONSES_CSV), exist_ok=True)
        is_new = not os.path.exists(BAD_RESPONSES_CSV)
        with open(BAD_RESPONSES_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(["timestamp", "restaurant_id", "prompt", "response", "reason"])
            writer.writerow([datetime.utcnow().isoformat(), restaurant_id, prompt, response, reason])
