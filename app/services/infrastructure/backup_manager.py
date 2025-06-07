import shutil, os
from datetime import datetime
from app.interfaces.infrastructure.backup_manager import BackupManager

class FileBackupManager(BackupManager):
    def backup_logs(self) -> None:
        log_dir = "app/logs"
        backup_dir = "backups"
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(backup_dir, f"logs_backup_{timestamp}")
        os.makedirs(dest, exist_ok=True)
        shutil.copytree(log_dir, dest, dirs_exist_ok=True)
