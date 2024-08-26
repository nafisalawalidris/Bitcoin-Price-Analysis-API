from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import psycopg2
import requests

# Database connection parameters
DATABASE_URL = "postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database"

# Pydantic model for request and response validation
class BitcoinPriceBase(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

class BitcoinPriceResponse(BitcoinPriceBase):
    id: int

app = FastAPI()

# Helper function to create a new database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.get("/prices/", response_model=List[BitcoinPriceResponse])
def get_all_prices():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bitcoin_prices")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Transforming the result to match the response model
    return [
        BitcoinPriceResponse(
            id=row[0], date=row[1], open=row[2], high=row[3], low=row[4],
            close=row[5], adj_close=row[6], volume=row[7]
        ) for row in rows
    ]

@app.get("/prices/{year}", response_model=List[BitcoinPriceResponse])
def get_prices_by_year(year: int):
    if year < 0:
        raise HTTPException(status_code=400, detail="Invalid year")
    
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bitcoin_prices WHERE date BETWEEN %s AND %s", (start_date, end_date))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not rows:
        raise HTTPException(status_code=404, detail="No prices found for the given year")

    return [
        BitcoinPriceResponse(
            id=row[0], date=row[1], open=row[2], high=row[3], low=row[4],
            close=row[5], adj_close=row[6], volume=row[7]
        ) for row in rows
    ]

@app.get("/prices/halving/{halving_number}", response_model=List[BitcoinPriceResponse])
def get_prices_by_halving(halving_number: int):
    halving_dates = {
        1: "2012-11-28",
        2: "2016-07-09",
        3: "2020-05-11",
        4: "2024-04-20",
    }

    if halving_number not in halving_dates:
        raise HTTPException(status_code=400, detail="Invalid halving number")

    start_date = halving_dates[halving_number]
    end_date = (pd.to_datetime(start_date) + pd.DateOffset(years=4)).strftime("%Y-%m-%d")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bitcoin_prices WHERE date BETWEEN %s AND %s", (start_date, end_date))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not rows:
        raise HTTPException(status_code=404, detail="No prices found for the given halving period")

    return [
        BitcoinPriceResponse(
            id=row[0], date=row[1], open=row[2], high=row[3], low=row[4],
            close=row[5], adj_close=row[6], volume=row[7]
        ) for row in rows
    ]

@app.get("/prices/halvings", response_model=List[BitcoinPriceResponse])
def get_prices_across_halvings():
    halving_dates = [
        "2012-11-28",
        "2016-07-09",
        "2020-05-11",
        "2024-04-20"
    ]

    conn = get_db_connection()
    cursor = conn.cursor()
    prices = []

    for start_date in halving_dates:
        end_date = (pd.to_datetime(start_date) + pd.DateOffset(years=4)).strftime("%Y-%m-%d")
        cursor.execute("SELECT * FROM bitcoin_prices WHERE date BETWEEN %s AND %s", (start_date, end_date))
        rows = cursor.fetchall()
        prices.extend(rows)

    cursor.close()
    conn.close()
    
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the halving periods")

    return [
        BitcoinPriceResponse(
            id=row[0], date=row[1], open=row[2], high=row[3], low=row[4],
            close=row[5], adj_close=row[6], volume=row[7]
        ) for row in prices
    ]

@app.get("/prices/bybit", response_model=BitcoinPriceBase)
def get_bybit_price():
    response = requests.get("https://api.bybit.com/v2/public/tickers")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from Bybit")
    data = response.json()
    if 'result' not in data:
        raise HTTPException(status_code=500, detail="Invalid response format from Bybit")
    price_data = data['result'][0]
    return BitcoinPriceBase(
        date=pd.to_datetime(price_data['timestamp']).strftime('%Y-%m-%d'),
        open=float(price_data['last_price']),
        high=float(price_data['high_price_24h']),
        low=float(price_data['low_price_24h']),
        close=float(price_data['last_price']),
        adj_close=float(price_data['last_price']),
        volume=float(price_data['volume_24h'])
    )

@app.get("/prices/binance", response_model=BitcoinPriceBase)
def get_binance_price():
    response = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from Binance")
    data = response.json()
    return BitcoinPriceBase(
        date=pd.to_datetime(data['closeTime'], unit='ms').strftime('%Y-%m-%d'),
        open=float(data['openPrice']),
        high=float(data['highPrice']),
        low=float(data['lowPrice']),
        close=float(data['lastPrice']),
        adj_close=float(data['lastPrice']),
        volume=float(data['volume'])
    )

@app.get("/prices/yahoo", response_model=BitcoinPriceBase)
def get_yahoo_price():
    response = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from Yahoo Finance")
    data = response.json()
    if 'chart' not in data or 'result' not in data['chart']:
        raise HTTPException(status_code=500, detail="Invalid response format from Yahoo Finance")
    result = data['chart']['result'][0]
    indicators = result['indicators']['quote'][0]
    timestamp = result['timestamp'][0]
    close_price = indicators['close'][0]
    date = pd.to_datetime(timestamp, unit='s').strftime('%Y-%m-%d')
    return BitcoinPriceBase(
        date=date,
        open=indicators['open'][0],
        high=indicators['high'][0],
        low=indicators['low'][0],
        close=close_price,
        adj_close=close_price,
        volume=indicators['volume'][0]
    )
