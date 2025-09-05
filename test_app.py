import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_get_festivals(client):
    response = client.get("/festivals")
    assert response.status_code == 200
    assert "results" in response.get_json()
