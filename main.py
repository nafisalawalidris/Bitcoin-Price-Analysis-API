from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
import pandas as pd
import requests
import yfinance as yf

# Create a FastAPI instance
app = FastAPI()

# Define the SQLAlchemy database URL
DATABASE_URL = "postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a SQLAlchemy session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a SQLAlchemy base class
Base = declarative_base()

# Define a SQLAlchemy model for Bitcoin price data
class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Float)

# Define a Pydantic model for Bitcoin price data
class BitcoinPriceBase(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

    class Config:
        orm_mode = True

# Define a response model that includes an ID for each price entry
class BitcoinPriceResponse(BitcoinPriceBase):
    id: int

# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to get all Bitcoin prices
@app.get("/prices/", response_model=List[BitcoinPriceResponse])
def get_all_prices(db: Session = Depends(get_db)):
    prices = db.query(BitcoinPrice).all()
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found.")
    return prices

# Endpoint to get Bitcoin prices for a specific year
@app.get("/prices/{year}", response_model=List[BitcoinPriceResponse])
def get_prices_by_year(year: int, db: Session = Depends(get_db)):
    if year < 0:
        raise HTTPException(status_code=400, detail="Invalid year. Year must be a positive integer.")
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    prices = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all()
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the given year")
    return prices

# Endpoint to get Bitcoin prices by halving number
@app.get("/prices/halving/{halving_number}", response_model=List[BitcoinPriceResponse])
def get_prices_by_halving(halving_number: int, db: Session = Depends(get_db)):
    halving_dates = {
        1: "2012-11-28",
        2: "2016-07-09",
        3: "2020-05-11",
        4: "2024-04-20",
    }
    if halving_number not in halving_dates:
        raise HTTPException(status_code=400, detail="Invalid halving number. Must be 1, 2, 3, or 4.")
    start_date = halving_dates[halving_number]
    end_date = (pd.to_datetime(start_date) + pd.DateOffset(years=4)).strftime("%Y-%m-%d")
    prices = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all()
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the given halving period")
    return prices

# Endpoint to get Bitcoin prices across all halving periods
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
        end_date = (pd.to_datetime(start_date) + pd.DateOffset(years=4)).strftime("%Y-%m-%d")
        prices.extend(db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all())
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the halving periods")
    return prices

# Endpoint to get Bitcoin price data from Bybit API
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
        high=float(price_data['last_price']),
        low=float(price_data['last_price']),
        close=float(price_data['last_price']),
        adj_close=float(price_data['last_price']),
        volume=float(price_data['volume_24h'])
    )

# Endpoint to get Bitcoin price data from Binance API
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

# Endpoint to get Bitcoin price data from Kraken API
@app.get("/prices/kraken", response_model=BitcoinPriceBase)
def get_kraken_price():
    response = requests.get("https://api.kraken.com/0/public/Ticker?pair=XBTUSD")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from Kraken")
    data = response.json()
    if 'result' not in data:
        raise HTTPException(status_code=500, detail="Invalid response format from Kraken")
    price_data = data['result']['XXBTZUSD']
    return BitcoinPriceBase(
        date=pd.to_datetime(price_data['time']).strftime('%Y-%m-%d'),
        open=float(price_data['o']),
        high=float(price_data['h'][0]),
        low=float(price_data['l'][0]),
        close=float(price_data['c'][0]),
        adj_close=float(price_data['c'][0]),
        volume=float(price_data['v'][0])
    )

# Endpoint to get Bitcoin price data from Yahoo Finance
@app.get("/prices/yahoo", response_model=List[BitcoinPriceBase])
def get_yahoo_prices():
    data = yf.download("BTC-USD", period="1y", interval="1d")
    if data.empty:
        raise HTTPException(status_code=404, detail="No data found from Yahoo Finance")
    return [
        BitcoinPriceBase(
            date=date.strftime('%Y-%m-%d'),
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            adj_close=row['Adj Close'],
            volume=row['Volume']
        )
        for date, row in data.iterrows()
    ]
