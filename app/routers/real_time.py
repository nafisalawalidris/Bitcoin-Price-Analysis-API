from fastapi import APIRouter, HTTPException
import requests
import logging

real_time_router = APIRouter()

@real_time_router.get("/some_endpoint")
def some_endpoint():
    return {"message": "This is a real-time bitcoin prices endpoint"}


# Define API endpoints for each exchange
BYBIT_API_URL = "https://api.bybit.com/v2/public/tickers?symbol=BTCUSD"
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
COINBASE_API_URL = "https://api.coinbase.com/v2/prices/bitcoin-usd/spot"
KUCOIN_API_URL = "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT"

# Helper functions to fetch real-time Bitcoin prices from each exchange
def fetch_bybit_price():
    try:
        response = requests.get(BYBIT_API_URL)
        response.raise_for_status()
        data = response.json()
        return data["result"][0]["last_price"]
    except requests.RequestException as e:
        logger.error(f"Error fetching Bybit price: {e}")
        raise HTTPException(status_code=500, detail="Error fetching Bybit price")

def fetch_binance_price():
    try:
        response = requests.get(BINANCE_API_URL)
        response.raise_for_status()
        data = response.json()
        return data["price"]
    except requests.RequestException as e:
        logger.error(f"Error fetching Binance price: {e}")
        raise HTTPException(status_code=500, detail="Error fetching Binance price")

def fetch_coinbase_price():
    try:
        response = requests.get(COINBASE_API_URL)
        response.raise_for_status()
        data = response.json()
        return data["data"]["amount"]
    except requests.RequestException as e:
        logger.error(f"Error fetching Coinbase price: {e}")
        raise HTTPException(status_code=500, detail="Error fetching Coinbase price")

def fetch_kucoin_price():
    try:
        response = requests.get(KUCOIN_API_URL)
        response.raise_for_status()
        data = response.json()
        return data["data"]["price"]
    except requests.RequestException as e:
        logger.error(f"Error fetching KuCoin price: {e}")
        raise HTTPException(status_code=500, detail="Error fetching KuCoin price")

# Endpoints to get Bitcoin prices from each exchange
@real_time_router.get("/prices/bybit", summary="Fetch latest Bitcoin price from Bybit")
def get_bybit_price():
    try:
        price = fetch_bybit_price()
        return {"source": "Bybit", "price": price}
    except HTTPException as e:
        raise e

@real_time_router.get("/prices/binance", summary="Fetch latest Bitcoin price from Binance")
def get_binance_price():
    try:
        price = fetch_binance_price()
        return {"source": "Binance", "price": price}
    except HTTPException as e:
        raise e

@real_time_router.get("/prices/coinbase", summary="Fetch latest Bitcoin price from Coinbase")
def get_coinbase_price():
    try:
        price = fetch_coinbase_price()
        return {"source": "Coinbase", "price": price}
    except HTTPException as e:
        raise e

@real_time_router.get("/prices/kucoin", summary="Fetch latest Bitcoin price from KuCoin")
def get_kucoin_price():
    try:
        price = fetch_kucoin_price()
        return {"source": "KuCoin", "price": price}
    except HTTPException as e:
        raise e
