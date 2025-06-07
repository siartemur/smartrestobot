# app/tests/test_chat.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)  # ✅ bu satır gereklidir

def test_chat_endpoint():
    payload = {
        "message": "Bugün vegan seçenekleriniz var mı?"
    }

    response = client.post("/api/chat", json=payload)  # ✅ doğru endpoint
    assert response.status_code == 200
    assert "response" in response.json()
    assert len(response.json()["response"]) > 10
