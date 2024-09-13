from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List, Any
from datetime import datetime
import logging

from app.database import get_db
from app.models.bitcoin_price import BitcoinPrice
from app.schema import StatisticsResponse, HalvingPricesResponse

# Set up logging
logger = logging.getLogger(__name__)
bitcoin_price_router = APIRouter()

@bitcoin_price_router.get("/prices/", response_model=List[dict], summary="Get All Historical Prices")
def get_all_prices(db: Session = Depends(get_db)):
    logger.info("Fetching all historical prices.")
    try:
        prices = db.query(BitcoinPrice).all()
        if not prices:
            logger.warning("No prices found in the database.")
            return []  # Return an empty list if no records are found
        return [price.to_dict() for price in prices]  # Return the list of prices directly
    except Exception as e:
        logger.error(f"Failed to fetch prices: {e}", exc_info=True)  # Log the full exception trace
        raise HTTPException(status_code=500, detail="Internal server error")

@bitcoin_price_router.get("/prices/{year}", response_model=List[dict], summary="Get Prices by Year")
def get_prices_by_year(year: int = Path(..., title="The year to fetch Bitcoin prices for"), db: Session = Depends(get_db)):
    logger.info(f"Fetching Bitcoin prices for year: {year}")
    try:
        # Query to get prices for the specific year
        prices = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(f'{year}-01-01', f'{year}-12-31')).all()
        if not prices:
            logger.warning(f"No prices found for the year {year}.")
            return []  # Return an empty list if no records are found
        return [price.to_dict() for price in prices]  # Return the list of prices directly
    except Exception as e:
        logger.error(f"Failed to fetch prices for year {year}: {e}", exc_info=True)  # Log the full exception trace
        raise HTTPException(status_code=500, detail="Internal server error")

@bitcoin_price_router.get("/prices/halving/{halving_number}", response_model=HalvingPricesResponse, summary="Get Prices Around Halving Events")
def read_prices_around_halving(halving_number: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Fetch Bitcoin prices around specific halving events."""
    logger.info(f"Fetching prices around halving number: {halving_number}.")

    # Define the halving dates and their ranges
    halving_dates: Dict[int, Dict[str, str]] = {
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
        logger.error(f"Error fetching prices for halving number {halving_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@bitcoin_price_router.get("/historical/prices/statistics", response_model=Dict[str, float], summary="Get Bitcoin Price Statistics")
def get_price_statistics(db: Session = Depends(get_db)):
    logger.info("Fetching Bitcoin price statistics.")
    try:
        # Aggregate statistics
        min_price = db.query(func.min(BitcoinPrice.low)).scalar()
        max_price = db.query(func.max(BitcoinPrice.high)).scalar()
        avg_price = db.query(func.avg(BitcoinPrice.close)).scalar()
        total_entries = db.query(func.count(BitcoinPrice.date)).scalar()

        return {
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": avg_price,
            "total_entries": total_entries
        }
    except Exception as e:
        logger.error(f"Failed to fetch price statistics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
