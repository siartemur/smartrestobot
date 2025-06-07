# app/services/core/metrics_logger.py

from app.services.core.logger_service import CSVLoggerService

# Logger servisini başlat
logger = CSVLoggerService()

# Dışarıdan çağrılabilir loglama fonksiyonu
def log_response_metrics(**kwargs) -> None:
    logger.log_response(**kwargs)
