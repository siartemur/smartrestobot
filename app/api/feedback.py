# app/api/feedback.py

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import csv
import os

router = APIRouter()

class FeedbackRequest(BaseModel):
    user_id: int
    message: str
    sentiment: str  # örnek: "positive", "neutral", "negative"

@router.post("/feedback")
def submit_feedback(feedback: FeedbackRequest):
    filepath = "app/logs/feedback.csv"
    file_exists = os.path.isfile(filepath)

    with open(filepath, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "user_id", "message", "sentiment"])
        writer.writerow([
            datetime.utcnow().isoformat(),
            feedback.user_id,
            feedback.message,
            feedback.sentiment
        ])

    return {"status": "success", "message": "Feedback submitted"}
