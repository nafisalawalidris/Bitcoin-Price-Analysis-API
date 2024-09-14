def test_get_price_from_coingecko():
    response = client.get("/api/coingecko")
    assert response.status_code == 200
    assert "price" in response.json()

def test_get_price_from_coincap():
    response = client.get("/api/coincap")
    assert response.status_code == 200
    assert "price" in response.json()

def test_get_price_from_binance():
    response = client.get("/api/binance")
    assert response.status_code == 200
    assert "price" in response.json()

def test_get_price_from_kraken():
    response = client.get("/api/kraken")
    assert response.status_code == 200
    assert "price" in response.json()
