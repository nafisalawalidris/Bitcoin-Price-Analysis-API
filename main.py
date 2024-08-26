from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
import pandas as pd
import requests

# Directly assign the database URL
DATABASE_URL = "postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database"

# Set up the SQLAlchemy database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, unique=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Float)

class BitcoinPriceBase(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

    class Config:
        from_attributes = True 

class BitcoinPriceResponse(BitcoinPriceBase):
    id: int

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/prices/", response_model=List[BitcoinPriceResponse])
def get_all_prices(db: Session = Depends(get_db)):
    prices = db.query(BitcoinPrice).all()
    return prices

@app.get("/prices/{year}", response_model=List[BitcoinPriceResponse])
def get_prices_by_year(year: int, db: Session = Depends(get_db)):
    if year < 0:
        raise HTTPException(status_code=400, detail="Invalid year")
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    prices = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all()
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the given year")
    return prices

@app.get("/prices/halving/{halving_number}", response_model=List[BitcoinPriceResponse])
def get_prices_by_halving(halving_number: int, db: Session = Depends(get_db)):
    halving_dates = {
        1: "2012-11-28",
        2: "2016-07-09",
        3: "2020-05-11",
        4: "2024-04-20",
    }

    if halving_number not in halving_dates:
        raise HTTPException(status_code=400, detail="Invalid halving number")

    start_date = halving_dates[halving_number]
    end_date = pd.to_datetime(start_date) + pd.DateOffset(years=4)
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Debug: Print start and end dates
    print(f"Fetching prices from {start_date} to {end_date_str}")

    prices = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date_str)).all()
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the given halving period")
    return prices

@app.get("/prices/halvings", response_model=List[BitcoinPriceResponse])
def get_prices_across_halvings(db: Session = Depends(get_db)):
    halving_dates = [
        "2012-11-28",
        "2016-07-09",
        "2020-05-11",
        "2024-04-20"
    ]
    
    prices = []
    for start_date in halving_dates:
        end_date = pd.to_datetime(start_date) + pd.DateOffset(years=4)
        end_date_str = end_date.strftime("%Y-%m-%d")
        prices.extend(db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date_str)).all())
    
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the halving periods")
    return prices

@app.get("/prices/bybit", response_model=BitcoinPriceBase)
def get_bybit_price():
    response = requests.get("https://api.bybit.com/v2/public/tickers")
    data = response.json()
    if response.status_code != 200 or 'result' not in data:
        raise HTTPException(status_code=500, detail="Error fetching data from Bybit")
    price_data = data['result'][0]  # Adjust based on response structure
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
    data = response.json()
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from Binance")
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
    data = response.json()
    if response.status_code != 200 or 'chart' not in data:
        raise HTTPException(status_code=500, detail="Error fetching data from Yahoo Finance")
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
