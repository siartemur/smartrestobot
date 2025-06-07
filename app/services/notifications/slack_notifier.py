import os
import httpx
from app.interfaces.notifications.notification_service import NotificationService

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")  # .env içinde tanımlı olmalı

class SlackNotifier(NotificationService):
    def send_email(self, to: str, subject: str, body: str) -> None:
        # E-posta servisi entegrasyonu henüz yapılmadı
        print(f"📧 E-posta gönder (TEST): To={to}, Subject={subject}, Body={body}")

    def send_slack_message(self, message: str) -> None:
        if not SLACK_WEBHOOK_URL:
            print("⚠️ SLACK_WEBHOOK_URL tanımlı değil.")
            return

        payload = {"text": message}

        try:
            response = httpx.post(SLACK_WEBHOOK_URL, json=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"🚨 Slack mesajı gönderilemedi: {e}")

# ✅ Dışarıdan doğrudan erişim için helper fonksiyon
notifier = SlackNotifier()

def send_slack_alert(message: str) -> None:
    notifier.send_slack_message(message)
