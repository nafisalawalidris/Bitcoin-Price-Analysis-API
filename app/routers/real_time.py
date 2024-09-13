from fastapi import APIRouter, HTTPException
import requests

real_time_router = APIRouter()

@real_time_router.get("/coingecko", summary="Fetch Bitcoin price from CoinGecko")
def get_coingecko_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        response.raise_for_status()
        data = response.json()
        return {"price": data["bitcoin"]["usd"]}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@real_time_router.get("/coincap", summary="Fetch Bitcoin price from CoinCap")
def get_coincap_price():
    try:
        response = requests.get("https://api.coincap.io/v2/assets/bitcoin")
        response.raise_for_status()
        data = response.json()
        return {"price": data["data"]["priceUsd"]}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@real_time_router.get("/binance", summary="Fetch Bitcoin price from Binance")
def get_binance_price():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        response.raise_for_status()
        data = response.json()
        return {"price": data["price"]}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@real_time_router.get("/kraken", summary="Fetch Bitcoin price from Kraken")
def get_kraken_price():
    try:
        response = requests.get("https://api.kraken.com/0/public/Ticker?pair=XXBTZUSD")
        response.raise_for_status()
        data = response.json()
        return {"price": data["result"]["XXBTZUSD"]["c"][0]}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
