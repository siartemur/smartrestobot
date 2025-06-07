# app/api/usage.py

from fastapi import APIRouter
import csv
from datetime import datetime
from typing import List

router = APIRouter()

@router.get("/usage")
def get_usage_data() -> List[dict]:
    usage_data = []
    try:
        with open("app/logs/usage.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                usage_data.append({
                    "timestamp": row.get("timestamp"),
                    "user_id": row.get("user_id"),
                    "restaurant_id": row.get("restaurant_id"),
                    "token_usage": row.get("token_usage"),
                    "latency_ms": row.get("latency_ms"),
                    "model": row.get("model"),
                })
    except FileNotFoundError:
        return {"error": "usage.csv not found"}

    return {"usage": usage_data}
