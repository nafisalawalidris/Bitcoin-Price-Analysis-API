from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test for the root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Bitcoin Price Analysis and Real-Time Data API"}

# Test for getting all historical prices
def test_get_all_prices():
    response = client.get("/api/prices/")
    assert response.status_code == 200
    # Adjust this to match the expected output of your API
    assert response.json() == [
        {"date": "2023-01-01", "price": 20000}
    ]

# Test for getting prices by year
def test_get_prices_by_year():
    response = client.get("/api/prices/2024")
    assert response.status_code == 200
    # Adjust this to match the expected output of your API
    assert response.json() == [
        {"date": "2024-01-01", "price": 20000}
    ]

# Test for getting prices around halving events
def test_get_prices_around_halving():
    response = client.get("/api/prices/halving/1")
    assert response.status_code == 200
    # Adjust this to match the expected output of your API
    assert response.json() == [
        {"date": "2020-05-11", "price": 9000}
    ]

# Test for getting Bitcoin price statistics
def test_get_price_statistics():
    response = client.get("/api/historical/prices/statistics")
    assert response.status_code == 200
    assert response.json() == {
        "average_price": 20000,
        "highest_price": 60000,
        "lowest_price": 3000
    }

# Test for fetching Bitcoin price from CoinGecko
def test_fetch_price_coingecko():
    response = client.get("/api/coingecko")
    assert response.status_code == 200
    assert response.json() == {"price": 20000}

# Test for fetching Bitcoin price from CoinCap
def test_fetch_price_coincap():
    response = client.get("/api/coincap")
    assert response.status_code == 200
    assert response.json() == {"price": 20000}

# Test for fetching Bitcoin price from Binance
def test_fetch_price_binance():
    response = client.get("/api/binance")
    assert response.status_code == 200
    assert response.json() == {"price": 20000}

# Test for fetching Bitcoin price from Kraken
def test_fetch_price_kraken():
    response = client.get("/api/kraken")
    assert response.status_code == 200
    assert response.json() == {"price": 20000}

# Optional: Add tests for bad requests and invalid data
def test_get_prices_by_invalid_year():
    response = client.get("/api/prices/abcd")
    assert response.status_code == 422  # Unprocessable Entity

def test_fetch_price_from_unavailable_source():
    response = client.get("/api/unknownsource")
    assert response.status_code == 404  # Not Found
