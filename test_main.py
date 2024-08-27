import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_prices():
    response = client.get("/prices/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure response is a list
    if response.json():  # Check only if there's any data returned
        assert "id" in response.json()[0]
        assert "date" in response.json()[0]

def test_get_prices_by_year():
    response = client.get("/prices/2023")
    assert response.status_code in [200, 404]  # Can be empty or filled
    if response.status_code == 200:
        assert isinstance(response.json(), list)
        assert "date" in response.json()[0]

def test_get_prices_by_invalid_year():
    response = client.get("/prices/-2023")
    assert response.status_code == 400

def test_get_prices_by_halving():
    response = client.get("/prices/halving/1")
    assert response.status_code in [200, 404]  # Can be empty or filled

def test_get_prices_invalid_halving():
    response = client.get("/prices/halving/5")
    assert response.status_code == 400

def test_get_bybit_price():
    response = client.get("/prices/bybit")
    assert response.status_code in [200, 500]  # Ensure status is either okay or error

def test_get_binance_price():
    response = client.get("/prices/binance")
    assert response.status_code in [200, 500]

def test_get_kraken_price():
    response = client.get("/prices/kraken")
    assert response.status_code in [200, 500]

def test_get_yahoo_prices():
    response = client.get("/prices/yahoo")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert isinstance(response.json(), list)
        if response.json():  # Check if data exists
            assert "date" in response.json()[0]
