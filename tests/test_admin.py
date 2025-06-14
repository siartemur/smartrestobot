import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Dummy JWT Token – test sırasında devre dışı kontrol varsa bu token istenebilir
DUMMY_JWT = "Bearer dummy-token"
HEADERS = {"Authorization": DUMMY_JWT}

def test_list_all_restaurants():
    response = client.get("/api/admin/restaurants", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_ab_test_report():
    response = client.get("/api/admin/ab-test-report")
    assert response.status_code == 200
    assert "results" in response.json()

def test_dashboard_page():
    response = client.get("/api/admin/dashboard")
    assert response.status_code == 200
    assert "<html>" in response.text
    assert "Yanıt Süresi" in response.text
    assert "Prompt vs Yanıt" in response.text

def test_bad_responses_dashboard():
    response = client.get("/api/admin/bad-responses")
    assert response.status_code == 200
    assert "<html>" in response.text
    assert "Kötü Yanıt Sayısı" in response.text
    assert "Kötü Yanıt Nedenleri" in response.text
