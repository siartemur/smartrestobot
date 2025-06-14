# tests/test_chat.py
from fastapi.testclient import TestClient
from app.main import app  # main.py içinde app = FastAPI() olmalı

client = TestClient(app)

def test_chat_response():
    payload = {
        "message": "Merhaba",
        "user_id": 1  # Gerekli alan eklendi
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    assert "response" in response.json()
