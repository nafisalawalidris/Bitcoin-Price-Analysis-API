from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, extract
from app.models import BitcoinPrice
from app.database import get_db 
from typing import List
import logging
import pandas as pd  

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Database configuration
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database'

# Set up the database connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
            "/prices/halving/{halving_number}": "Provides Bitcoin price data around specific halving events",
            "/prices/halvings": "Retrieves Bitcoin prices across all halving periods"
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
    halving_dates = {
        1: {"date": "2012-11-28", "start": "2012-09-01", "end": "2013-02-28"},
        2: {"date": "2016-07-09", "start": "2016-04-01", "end": "2016-10-31"},
        3: {"date": "2020-05-11", "start": "2020-02-01", "end": "2020-08-31"},
        4: {"date": "2024-04-19", "start": "2024-02-01", "end": "2024-08-31"}
    }

    if halving_number not in halving_dates:
        logger.error(f"Halving event {halving_number} not found")
        raise HTTPException(status_code=404, detail="Halving event not found")

    date_range = halving_dates[halving_number]
    date_range_start = date_range["start"]
    date_range_end = date_range["end"]
    
    logger.info(f"Date range: {date_range_start} to {date_range_end}")
    
    prices = db.query(BitcoinPrice).filter(
        BitcoinPrice.date.between(date_range_start, date_range_end)
    ).all()

    if not prices:
        logger.error("No price data available for the specified halving event")
        raise HTTPException(status_code=404, detail="No price data available for the specified halving event")

    return {"halving_number": halving_number, "prices": [price.to_dict() for price in prices]}
