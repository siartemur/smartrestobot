def test_root_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "SmartRestoBot" in response.text