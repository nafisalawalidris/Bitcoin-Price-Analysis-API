from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.main.fetch_price_from_coingecko")
def test_mocked_price_from_coingecko(mock_fetch_price):
    # Mock response
    mock_fetch_price.return_value = {"price": 50000}
    response = client.get("/api/coingecko")
    assert response.status_code == 200
    assert response.json() == {"price": 50000}

@patch("app.main.fetch_price_from_coincap")
def test_mocked_price_from_coincap(mock_fetch_price):
    # Mock response
    mock_fetch_price.return_value = {"price": 51000}
    response = client.get("/api/coincap")
    assert response.status_code == 200
    assert response.json() == {"price": 51000}

@patch("app.main.fetch_price_from_binance")
def test_mocked_price_from_binance(mock_fetch_price):
    # Mock response
    mock_fetch_price.return_value = {"price": 52000}
    response = client.get("/api/binance")
    assert response.status_code == 200
    assert response.json() == {"price": 52000}

@patch("app.main.fetch_price_from_kraken")
def test_mocked_price_from_kraken(mock_fetch_price):
    # Mock response
    mock_fetch_price.return_value = {"price": 53000}
    response = client.get("/api/kraken")
    assert response.status_code == 200
    assert response.json() == {"price": 53000}
