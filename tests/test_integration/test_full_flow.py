from datetime import datetime


def test_full_user_flow(client):
    now = datetime.utcnow().isoformat().replace(":", "").replace(".", "")
    email = f"user_{now}@test.com"
    password = "Pass123!"

    register = client.post("/api/auth/register", json={
        "email": email,
        "password": password,
        "name": "User Test"
    })

    assert register.status_code in (200, 201)

    data = register.json()
    assert "email" in data
    assert data["email"] == email
