from typing import Protocol

class NotificationService(Protocol):
    def send_email(self, to: str, subject: str, body: str) -> None:
        ...

    def send_slack_message(self, message: str) -> None:
        ...
