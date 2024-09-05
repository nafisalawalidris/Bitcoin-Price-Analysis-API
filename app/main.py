from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, extract
from app.models import BitcoinPrice, Base
from app.database import get_db
import logging
from pydantic import BaseModel
from typing import List, Optional



# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define response models
class Price(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int

class HalvingPricesResponse(BaseModel):
    halving_number: int
    prices: List[Price]

# Create FastAPI instance
app = FastAPI(
    title="Bitcoin Price Analysis and Real-Time Data API",
    version="0.1.0",
    description="The Bitcoin Price Analysis and Real-Time Data API is an open-source API project designed to provide accurate, up-to-date and comprehensive Bitcoin pricing data for developers, researchers and financial analysts. Built on the robust FastAPI framework, this API offers seamless integration and high-performance endpoints for users who require real-time and historical Bitcoin price information. With Bitcoin being one of the most volatile and widely traded digital assets access to reliable price data is critical for informed decision-making in trading, investment and market analysis. This API serves as a one-stop solution delivering data in a highly organised format that is easy to consume and use in various applications.",
    contact={
        "name": "Nafisa Lawal Idris",
        "portfolio": "https://nafisalawalidris.github.io/13/",
    },
    license_info={
        "name": "MIT",
    },
)

# Database configuration
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database'

# Set up the database connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Event handlers for startup and shutdown
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application.")
    # Add any startup logic here

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application.")
    # Add any shutdown logic here

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bitcoin Price API"}

@app.get("/root/")
def read_root_details():
    return {
        "overview": "This API provides various endpoints to access historical Bitcoin price data.",
        "endpoints": {
            "/prices/": "Retrieves all historical Bitcoin prices",
            "/prices/{year}": "Fetches Bitcoin prices for a specific year",
            "/prices/halving/{halving_number}": "Provides Bitcoin price data around specific halving events"
        }
    }

@app.get("/prices/")
def get_all_prices(db: Session = Depends(get_db)):
    logger.info("Fetching all prices.")
    prices = db.query(BitcoinPrice).all()
    return {"prices": [price.to_dict() for price in prices]}

@app.get("/prices/{year}")
def get_prices_by_year(year: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching prices for year: {year}.")
    prices = db.query(BitcoinPrice).filter(extract('year', BitcoinPrice.date) == year).all()
    if not prices:
        raise HTTPException(status_code=404, detail="No price data found for the specified year.")
    return {"prices": [price.to_dict() for price in prices]}

@app.get("/prices/halving/{halving_number}")
def read_prices_around_halving(halving_number: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching prices around halving number: {halving_number}")
    
    # Define the halving dates
    halving_dates = {
        1: {"date": "2012-11-28", "start": "2012-09-01", "end": "2013-02-28"},
        2: {"date": "2016-07-09", "start": "2016-04-01", "end": "2016-10-31"},
        3: {"date": "2020-05-11", "start": "2020-02-01", "end": "2020-08-31"},
        4: {"date": "2024-04-19", "start": "2024-02-01", "end": "2024-08-31"}
    }

    # Check if the halving number is valid
    if halving_number not in halving_dates:
        logger.error(f"Halving event {halving_number} not found")
        raise HTTPException(status_code=404, detail="Halving event not found")

    date_range = halving_dates[halving_number]
    date_range_start = date_range["start"]
    date_range_end = date_range["end"]
    
    logger.info(f"Date range: {date_range_start} to {date_range_end}")
    
    try:
        # Query the database
        prices = db.query(BitcoinPrice).filter(
            BitcoinPrice.date.between(date_range_start, date_range_end)
        ).all()
    except Exception as e:
        logger.error(f"Database query failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    if not prices:
        logger.error("No price data available for the specified halving event")
        raise HTTPException(status_code=404, detail="No price data available for the specified halving event")

    return {"halving_number": halving_number, "prices": [price.to_dict() for price in prices]}
