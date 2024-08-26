# Import statements at the top of the file
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app from the main module

# Initialize TestClient
client = TestClient(app)

# Test cases
def test_get_all_prices():
    response = client.get("/prices/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_prices_by_year():
    response = client.get("/prices/2022")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_prices_by_halving():
    response = client.get("/prices/halving/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_prices_across_halvings():
    response = client.get("/prices/halvings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_bybit_price():
    response = client.get("/prices/bybit")
    assert response.status_code == 200
    assert "date" in response.json()

def test_get_binance_price():
    response = client.get("/prices/binance")
    assert response.status_code == 200
    assert "date" in response.json()

def test_get_yahoo_price():
    response = client.get("/prices/yahoo")
    assert response.status_code == 200
    assert "date" in response.json()
