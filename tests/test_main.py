import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Bitcoin Price API"}

def test_read_root_details():
    response = client.get("/root/")
    assert response.status_code == 200
    assert response.json() == {
        "overview": "This API provides various endpoints to access historical Bitcoin price data.",
        "endpoints": {
            "/prices/": "Retrieves all historical Bitcoin prices",
            "/prices/{year}": "Fetches Bitcoin prices for a specific year",
            "/prices/halving/{halving_number}": "Provides Bitcoin price data around specific halving events",
            "/prices/halvings": "Retrieves Bitcoin prices across all halving periods"
        }
    }

def test_get_all_prices():
    # Assuming you have some sample data loaded in your test database
    response = client.get("/prices/")
    assert response.status_code == 200
    assert isinstance(response.json()["prices"], list)

def test_get_prices_by_year():
    # Test for a year with expected data
    response = client.get("/prices/2023")
    assert response.status_code == 200
    assert isinstance(response.json()["prices"], list)

    # Test for a year with no data
    response = client.get("/prices/1900")
    assert response.status_code == 404

def test_read_prices_around_halving():
    response = client.get("/prices/halving/1")
    assert response.status_code == 200
    data = response.json()
    assert "halving_number" in data
    assert data["halving_number"] == 1
    assert "prices" in data
    assert isinstance(data["prices"], list)