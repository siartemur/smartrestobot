import os
import csv
from app.interfaces.core.metrics_reader import MetricsReader

METRICS_FILE = "app/logs/metrics.csv"

class CSVReaderService(MetricsReader):
    def show_metrics_summary(self) -> None:
        if not os.path.exists(METRICS_FILE):
            print("📭 Henüz kayıtlı metrik yok.")
            return

        with open(METRICS_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            print("\n📊 METRİK KAYITLARI\n-------------------------")
            for row in reader:
                print(f"Tarih: {row.get('timestamp')}")
                print(f"Prompt Versiyonu: {row.get('prompt_version')}")
                print(f"Yanıt Süresi (ms): {row.get('latency_ms')}")
                print(f"Kullanılan Token: {row.get('token_usage')}")
                print(f"Kalitesiz Yanıt mı?: {row.get('bad_response')}")
                print("-------------------------")
