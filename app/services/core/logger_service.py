from app.services.core.csv_logger import CSVLoggerService

logger = CSVLoggerService()

def log_response_metrics(**kwargs) -> None:
    logger.log_response(**kwargs)
