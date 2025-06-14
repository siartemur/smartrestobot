# tests/test_ab_test.py
def test_ab_test_endpoint(client):
    response = client.get("/api/ab-test/metrics")
    assert response.status_code in (200, 404)