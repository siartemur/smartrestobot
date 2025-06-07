from typing import Protocol

class BackupManager(Protocol):
    def backup_logs(self) -> None:
        ...
