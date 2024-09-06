from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract
from datetime import datetime
from typing import List
import logging

from app.database import get_db
from app.models.bitcoin_price import BitcoinPrice
from app.schema import HalvingPricesResponse, Price

# Set up logging
logger = logging.getLogger(__name__)
bitcoin_price_router = APIRouter()

@bitcoin_price_router.get("/", summary="Root Endpoint")
def read_root():
    logger.info("Accessed the root endpoint.")
    return {"message": "Welcome to the Bitcoin Price API. Please visit /api/0.1.0/prices/ for API endpoints."}

@bitcoin_price_router.get("/root/", summary="Root Details")
def read_root_details():
    logger.info("Accessed the root details endpoint.")
    return {
        "overview": "This API provides various endpoints to access historical Bitcoin price data.",
        "endpoints": {
            "/prices/": "Retrieves all historical Bitcoin prices",
            "/prices/{year}": "Fetches Bitcoin prices for a specific year",
            "/prices/halving/{halving_number}": "Provides Bitcoin price data around specific halving events"
        }
    }

@bitcoin_price_router.get("/prices/", response_model=List[Price], summary="Get All Historical Prices")
def get_all_prices(db: Session = Depends(get_db)):
    logger.info("Fetching all historical prices.")
    try:
        prices = db.query(BitcoinPrice).all()
        if not prices:
            logger.warning("No prices found in the database.")
            return {"prices": []}
        return {"prices": [price.to_dict() for price in prices]}
    except Exception as e:
        logger.error(f"Failed to fetch prices: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@bitcoin_price_router.get("/prices/{year}", response_model=List[Price], summary="Get Prices by Year")
def get_prices_by_year(year: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching prices for year: {year}.")
    try:
        prices = db.query(BitcoinPrice).filter(extract('year', BitcoinPrice.date) == year).all()
        if not prices:
            logger.warning(f"No price data found for year: {year}.")
            raise HTTPException(status_code=404, detail="No price data found for the specified year.")
        return {"prices": [price.to_dict() for price in prices]}
    except Exception as e:
        logger.error(f"Failed to fetch prices for year {year}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@bitcoin_price_router.get("/prices/halving/{halving_number}", response_model=HalvingPricesResponse, summary="Get Prices Around Halving Events")
def read_prices_around_halving(halving_number: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching prices around halving number: {halving_number}.")

    # Define the halving dates
    halving_dates = {
        1: {"date": "2012-11-28", "start": "2012-09-01", "end": "2013-02-28"},
        2: {"date": "2016-07-09", "start": "2016-04-01", "end": "2016-10-31"},
        3: {"date": "2020-05-11", "start": "2020-02-01", "end": "2020-08-31"},
        4: {"date": "2024-04-19", "start": "2024-02-01", "end": "2024-08-31"}
    }

    if halving_number not in halving_dates:
        logger.error(f"Halving event {halving_number} not found.")
        raise HTTPException(status_code=404, detail="Halving event not found")

    date_range = halving_dates[halving_number]
    date_range_start = datetime.strptime(date_range["start"], "%Y-%m-%d").date()
    date_range_end = datetime.strptime(date_range["end"], "%Y-%m-%d").date()

    logger.info(f"Date range for halving number {halving_number}: {date_range_start} to {date_range_end}")

    try:
        prices = db.query(BitcoinPrice).filter(
            BitcoinPrice.date.between(date_range_start, date_range_end)
        ).all()
        if not prices:
            logger.warning(f"No price data available for halving number: {halving_number}")
            raise HTTPException(status_code=404, detail="No price data available for the specified halving event.")
        return {"halving_number": halving_number, "prices": [price.to_dict() for price in prices]}
    except Exception as e:
        logger.error(f"Database query failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
