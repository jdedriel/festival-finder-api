import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

# Test /festivals with region filter
def test_get_festivals_by_region(client):
    response = client.get("/festivals?region=Central Visayas")
    assert response.status_code == 200
    data = response.get_json()
    assert "results" in data
    assert data["count"] >= 1

# Test /festivals with month filter
def test_get_festivals_by_month(client):
    response = client.get("/festivals?month=1")
    assert response.status_code == 200
    data = response.get_json()
    assert "results" in data
    assert data["count"] >= 1

# Test /festivals/<id> with valid ID
def test_get_festival_by_id(client):
    response = client.get("/festivals/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert "name" in data

# Test /festivals/<id> with invalid ID
def test_get_festival_invalid_id(client):
    response = client.get("/festivals/999")
    assert response.status_code == 404

# Test /recommend with valid festival_id
def test_recommend_valid(client):
    response = client.get("/recommend?festival_id=1")
    assert response.status_code == 200
    data = response.get_json()
    assert "recommendations" in data
    assert len(data["recommendations"]) == 3

# Test /recommend with missing festival_id
def test_recommend_missing_id(client):
    response = client.get("/recommend")
    assert response.status_code == 400

# Test /regions endpoint
def test_get_regions(client):
    response = client.get("/regions")
    assert response.status_code == 200
    data = response.get_json()
    assert "regions" in data
    assert isinstance(data["regions"], list)

# Test /months endpoint
def test_get_months(client):
    response = client.get("/months")
    assert response.status_code == 200
    data = response.get_json()
    assert "months" in data
    assert isinstance(data["months"], list)
