from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal, get_db
import pandas as pd
import yfinance as yf  
import requests  

# Create a FastAPI instance
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Define Pydantic models for request and response handling
class BitcoinPriceBase(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

class BitcoinPriceResponse(BaseModel):
    prices: List[BitcoinPriceBase]

@app.get("/prices/", response_model=List[BitcoinPriceBase])
def get_all_prices(db: Session = Depends(get_db)):
    print("success") 
    prices = db.query(models.BitcoinPrice).all()  
    return []  

@app.get("/prices/{year}", response_model=List[BitcoinPriceBase])
def get_prices_by_year(year: int, db: Session = Depends(get_db)):
    print("success")  
    if year < 0:
        raise HTTPException(status_code=400, detail="Year must be a positive integer")
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    return [] 

@app.get("/prices/halving/{halving_number}", response_model=List[BitcoinPriceBase])
def get_prices_by_halving(halving_number: int, db: Session = Depends(get_db)):
    print("success")  
    halving_dates = {
        1: "2012-11-28",
        2: "2016-07-09",
        3: "2020-05-11",
        4: "2024-04-20",
    }
    if halving_number not in halving_dates:
        raise HTTPException(status_code=400, detail="Invalid halving number")
    return [] 

@app.get("/prices/halvings", response_model=List[BitcoinPriceBase])
def get_prices_across_halvings(db: Session = Depends(get_db)):
    print("success")
    halving_dates = [
        "2012-11-28",
        "2016-07-09",
        "2020-05-11",
        "2024-04-20"
    ]
    prices = []
    return prices

def fetch_price_from_api(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    return response.json()

@app.get("/prices/bybit", response_model=BitcoinPriceBase)
def get_bybit_price():
    print("success")
    url = "https://api.bybit.com/v2/public/tickers?symbol=BTCUSD"
    data = fetch_price_from_api(url)
    price_data = data['result'][0]
    return BitcoinPriceBase(
        date=pd.to_datetime(price_data['timestamp']).strftime('%Y-%m-%d'),
        open=float(price_data['last_price']),
        high=float(price_data['last_price']),
        low=float(price_data['last_price']),
        close=float(price_data['last_price']),
        adj_close=float(price_data['last_price']),
        volume=float(price_data['volume_24h'])
    )

@app.get("/prices/binance", response_model=BitcoinPriceBase)
def get_binance_price():
    print("success")
    url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
    data = fetch_price_from_api(url)
    return BitcoinPriceBase(
        date=pd.to_datetime(data['closeTime'], unit='ms').strftime('%Y-%m-%d'),
        open=float(data['openPrice']),
        high=float(data['highPrice']),
        low=float(data['lowPrice']),
        close=float(data['lastPrice']),
        adj_close=float(data['lastPrice']),
        volume=float(data['volume'])
    )

@app.get("/prices/kraken", response_model=BitcoinPriceBase)
def get_kraken_price():
    print("success")
    url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
    data = fetch_price_from_api(url)
    price_data = data['result']['XXBTZUSD']
    return BitcoinPriceBase(
        date=pd.to_datetime(price_data['c'][0]).strftime('%Y-%m-%d'),
        open=float(price_data['o'][0]),
        high=float(price_data['h'][0]),
        low=float(price_data['l'][0]),
        close=float(price_data['c'][0]),
        adj_close=float(price_data['c'][0]),
        volume=float(price_data['v'][0])
    )

@app.get("/prices/yahoo", response_model=List[BitcoinPriceBase])
def get_yahoo_prices():
    print("success")
    data = yf.download("BTC-USD", period="1y", interval="1d")
    yahoo_prices = []
    for index, row in data.iterrows():
        yahoo_prices.append(BitcoinPriceBase(
            date=index.strftime("%Y-%m-%d"),
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            adj_close=row['Adj Close'],
            volume=row['Volume']
        ))
    return yahoo_prices
