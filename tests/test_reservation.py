# tests/test_reservation.py
def test_create_reservation(client):
    payload = {
        "user_id": 1,
        "restaurant_id": "rest_001",
        "date": "2025-06-10",
        "time": "19:00",
        "people": 4
    }
    response = client.post("/api/reservation", json=payload)
    assert response.status_code in (200, 201)
    assert "rezervasyon alındı" in response.json()["message"]



