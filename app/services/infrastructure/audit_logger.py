import csv, os
from datetime import datetime
from app.interfaces.infrastructure.audit_logger import AuditLogger

LOG_FILE = "app/logs/audit_logs.csv"

class CSVLogger(AuditLogger):
    def log_interaction(self, user_id: int, message: str, response: str, agent_type: str) -> None:
        os.makedirs("app/logs", exist_ok=True)
        file_exists = os.path.isfile(LOG_FILE)
        with open(LOG_FILE, mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["timestamp", "user_id", "message", "response", "agent_type"])
            writer.writerow([datetime.utcnow().isoformat(), user_id, message, response, agent_type])
