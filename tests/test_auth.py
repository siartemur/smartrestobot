import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    response = client.post("/api/auth/register", json={
        "name": "Test User",
        "email": unique_email,
        "password": "Test1234"
    })
    assert response.status_code in (200, 201)

def test_login_user():
    # Bu testte sabit kullanıcı bilgisi girilmişse önce register edilmelidir
    email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    password = "Test1234"

    # Önce register
    client.post("/api/auth/register", json={
        "name": "Login User",
        "email": email,
        "password": password
    })

    # Sonra login
    response = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
