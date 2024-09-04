import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, extract
from app.models import BitcoinPrice, Base
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
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
def get_prices_around_halving(halving_number: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching prices around halving event number: {halving_number}.")
    halving_dates = {
        1: {"date": "2012-11-28", "start": "2012-09-01", "end": "2013-02-28"},
        2: {"date": "2016-07-09", "start": "2016-04-01", "end": "2016-10-31"},
        3: {"date": "2020-05-11", "start": "2020-02-01", "end": "2020-08-31"},
        4: {"date": "2024-04-19", "start": "2024-02-01", "end": "2024-08-31"}
    }
    
    if halving_number not in halving_dates:
        raise HTTPException(status_code=404, detail="Invalid halving number.")
    
    dates = halving_dates[halving_number]
    prices = db.query(BitcoinPrice).filter(
        BitcoinPrice.date.between(dates["start"], dates["end"])
    ).all()
    
    if not prices:
        raise HTTPException(status_code=404, detail="No price data found around the specified halving event.")
    
    return {"prices": [price.to_dict() for price in prices]}

@app.get("/prices/halvings")
def get_prices_across_halvings(db: Session = Depends(get_db)):
    logger.info("Fetching prices across all halving periods.")
    
    halving_dates = [
        {"date": "2012-11-28", "start": "2012-09-01", "end": "2013-02-28"},
        {"date": "2016-07-09", "start": "2016-04-01", "end": "2016-10-31"},
        {"date": "2020-05-11", "start": "2020-02-01", "end": "2020-08-31"}
    ]
    
    prices = []
    
    try:
        for halving in halving_dates:
            halving_prices = db.query(BitcoinPrice).filter(
                BitcoinPrice.date.between(halving["start"], halving["end"])
            ).all()
            prices.extend(halving_prices)
    
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return {"prices": [price.to_dict() for price in prices]}