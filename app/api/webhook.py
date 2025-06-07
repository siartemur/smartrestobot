from fastapi import APIRouter, Request
import logging

router = APIRouter()

@router.post("/webhook/slack")
async def slack_webhook(request: Request):
    """
    Slack Webhook için FastAPI endpoint.
    Dış sistemler (veya local tetikleyiciler) tarafından çağrılır.
    """
    data = await request.json()
    message = data.get("message")

    if not message:
        return {"status": "error", "detail": "No message provided."}

    # (İstersen buraya loglama da eklersin)
    logging.info(f"Slack mesajı alındı: {message}")
    return {"status": "ok", "received": message}
