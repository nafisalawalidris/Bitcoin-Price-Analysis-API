from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, validator
from sqlalchemy import create_engine, Column, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
import logging
import yfinance as yf
from datetime import date
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize logging to monitor application events and errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database")

# Create a SQLAlchemy engine for database connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()

# Define SQLAlchemy model for Bitcoin prices
class BitcoinPrice(Base):
    __tablename__ = 'bitcoin_prices'
    date = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Float)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create FastAPI app instance
app = FastAPI()

# Define Pydantic models for request and response handling
class BitcoinPriceBase(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

    @validator('volume')
    def check_volume_positive(cls, v):
        if v < 0:
            raise ValueError('Volume must be positive')
        return v

class BitcoinPriceCreate(BitcoinPriceBase):
    pass

class BitcoinPriceResponse(BitcoinPriceBase):
    class Config:
        orm_mode = True

# Function to fetch data from an API
def fetch_price_from_api(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch data from API")

# Define endpoints
@app.get("/prices/", response_model=List[BitcoinPriceBase])
def get_all_prices(db: Session = Depends(get_db)):
    logger.info("Endpoint /prices/ was accessed")
    prices = db.query(BitcoinPrice).all()
    return prices

@app.get("/prices/{year}", response_model=List[BitcoinPriceBase])
def get_prices_by_year(year: int, db: Session = Depends(get_db)):
    logger.info(f"Endpoint /prices/{year} was accessed")
    if year < 0:
        raise HTTPException(status_code=400, detail="Year must be a positive integer")
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    prices_by_year = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all()
    return prices_by_year

@app.get("/prices/halving/{halving_number}", response_model=List[BitcoinPriceBase])
def get_prices_by_halving(halving_number: int, db: Session = Depends(get_db)):
    logger.info(f"Endpoint /prices/halving/{halving_number} was accessed")
    halving_dates = {
        1: "2012-11-28",
        2: "2016-07-09",
        3: "2020-05-11",
        4: "2024-04-20",
    }
    if halving_number not in halving_dates:
        raise HTTPException(status_code=400, detail="Invalid halving number")
    halving_date = halving_dates[halving_number]
    prices_by_halving = db.query(BitcoinPrice).filter(BitcoinPrice.date >= halving_date).all()
    return prices_by_halving

@app.get("/prices/halvings", response_model=List[BitcoinPriceBase])
def get_prices_across_halvings(db: Session = Depends(get_db)):
    logger.info("Endpoint /prices/halvings was accessed")
    halving_dates = [
        "2012-11-28",
        "2016-07-09",
        "2020-05-11",
        "2024-04-20"
    ]
    prices_across_halvings = []
    for date in halving_dates:
        prices = db.query(BitcoinPrice).filter(BitcoinPrice.date >= date).all()
        prices_across_halvings.extend(prices)
    return prices_across_halvings

@app.get("/prices/bybit", response_model=BitcoinPriceBase)
def get_bybit_price():
    logger.info("Endpoint /prices/bybit was accessed")
    url = "https://api.bybit.com/v2/public/tickers?symbol=BTCUSD"
    data = fetch_price_from_api(url)
    price_data = data['result'][0]
    bybit_price = BitcoinPriceBase(
        date=date.today(),  # Use the current date
        open=float(price_data['last_price']),
        high=float(price_data['last_price']),
        low=float(price_data['last_price']),
        close=float(price_data['last_price']),
        adj_close=float(price_data['last_price']),
        volume=float(price_data['volume_24h'])
    )
    return bybit_price

@app.get("/prices/binance", response_model=BitcoinPriceBase)
def get_binance_price():
    logger.info("Endpoint /prices/binance was accessed")
    url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
    data = fetch_price_from_api(url)
    binance_price = BitcoinPriceBase(
        date=date.today(),  # Use the current date
        open=float(data['openPrice']),
        high=float(data['highPrice']),
        low=float(data['lowPrice']),
        close=float(data['lastPrice']),
        adj_close=float(data['lastPrice']),
        volume=float(data['volume'])
    )
    return binance_price

@app.get("/prices/kraken", response_model=BitcoinPriceBase)
def get_kraken_price():
    logger.info("Endpoint /prices/kraken was accessed")
    url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
    data = fetch_price_from_api(url)
    price_data = data['result']['XXBTZUSD']
    kraken_price = BitcoinPriceBase(
        date=date.today(),  # Use the current date
        open=float(price_data['o'][0]),
        high=float(price_data['h'][0]),
        low=float(price_data['l'][0]),
        close=float(price_data['c'][0]),
        adj_close=float(price_data['c'][0]),
        volume=float(price_data['v'][0])
    )
    return kraken_price

@app.get("/prices/yahoo", response_model=List[BitcoinPriceBase])
def get_yahoo_prices():
    logger.info("Endpoint /prices/yahoo was accessed")
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

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup: checking database connection...")
    try:
        conn = psycopg2.connect(
            dbname="Bitcoin_Prices_Database",
            user="postgres",
            password=os.getenv("DB_PASSWORD", "password"),
            host="localhost",
            port="5432"
        )
        conn.close()
        logger.info("Successfully connected to the database.")
    except psycopg2.OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")

# Run the FastAPI app using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
