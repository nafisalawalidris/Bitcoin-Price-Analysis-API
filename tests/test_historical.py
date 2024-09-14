from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_all_prices():
    response = client.get("/historical/prices/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_prices_by_year():
    response = client.get("/historical/prices/2024")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_prices_around_halving():
    response = client.get("/historical/prices/halving/2")
    assert response.status_code == 200
    assert "halving_number" in response.json()

def test_get_price_statistics():
    response = client.get("/historical/prices/statistics")
    assert response.status_code == 200
    assert "min_price" in response.json()
