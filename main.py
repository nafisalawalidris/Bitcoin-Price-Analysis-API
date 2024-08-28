# main.py

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import inspect
import pandas as pd
import requests
import yfinance as yf
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Define Pydantic models for Bitcoin price data
class BitcoinPriceBase(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

class BitcoinPriceCreate(BitcoinPriceBase):
    pass

class BitcoinPriceResponse(BitcoinPriceBase):
    id: int

    class Config:
        orm_mode = True

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialise database on startup
@app.on_event("startup")
def on_startup():
    # Create tables in the database if they do not exist
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    logger.info(f"Tables in database: {tables}")
    columns = inspector.get_columns('bitcoin_prices')
    logger.info(f"Columns in bitcoin_prices: {columns}")

@app.get("/prices/", response_model=List[BitcoinPriceResponse])
def get_all_prices(db: Session = Depends(get_db)):
    try:
        prices = db.query(BitcoinPrice).all()
        if not prices:
            raise HTTPException(status_code=404, detail="No prices found.")
        return prices
    except Exception as e:
        logger.error(f"Error fetching all prices: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/prices/{year}", response_model=List[BitcoinPriceResponse])
def get_prices_by_year(year: int, db: Session = Depends(get_db)):
    if year < 0:
        raise HTTPException(status_code=400, detail="Invalid year. Year must be a positive integer.")
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    try:
        prices = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all()
        if not prices:
            raise HTTPException(status_code=404, detail="No prices found for the given year")
        return prices
    except Exception as e:
        logger.error(f"Error fetching prices by year {year}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

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
    try:
        prices = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all()
        if not prices:
            raise HTTPException(status_code=404, detail="No prices found for the given halving period")
        return prices
    except Exception as e:
        logger.error(f"Error fetching prices by halving {halving_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/prices/halvings", response_model=List[BitcoinPriceResponse])
def get_prices_across_halvings(db: Session = Depends(get_db)):
    halving_dates = [
        "2012-11-28",
        "2016-07-09",
        "2020-05-11",
        "2024-04-20"
    ]
    prices = []
    try:
        for start_date in halving_dates:
            end_date = (pd.to_datetime(start_date) + pd.DateOffset(years=4)).strftime("%Y-%m-%d")
            prices.extend(db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all())
        if not prices:
            raise HTTPException(status_code=404, detail="No prices found for the halving periods")
        return prices
    except Exception as e:
        logger.error(f"Error fetching prices across halvings: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def fetch_price_from_api(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from API {url}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching data from API")

@app.get("/prices/bybit", response_model=BitcoinPriceBase)
def get_bybit_price():
    url = "https://api.bybit.com/v2/public/tickers?symbol=BTCUSD"
    data = fetch_price_from_api(url)
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

@app.get("/prices/binance", response_model=BitcoinPriceBase)
def get_binance_price():
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
    url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
    data = fetch_price_from_api(url)
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

@app.get("/prices/yahoo", response_model=List[BitcoinPriceBase])
def get_yahoo_prices():
    data = yf.download("BTC-USD", period="1y", interval="1d")
    if data.empty:
        raise HTTPException(status_code=404, detail="No price data found from Yahoo Finance.")
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
