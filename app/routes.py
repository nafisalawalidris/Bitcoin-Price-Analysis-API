from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models import Price
from app.database import get_db
from app.crud import (
    get_all_prices,
    get_price_by_year,
    get_prices_by_halving,
    get_prices_across_halvings,
    get_bybit_price,
    get_binance_price,
    get_kraken_price,
    get_yahoo_price
)

# Create the API Router
router = APIRouter()

@router.get("/prices/", response_model=List[Price])
def read_all_prices(db: Session = Depends(get_db)):
    """
    Retrieve all Bitcoin price records.
    """
    prices = get_all_prices(db)
    return prices

@router.get("/prices/year/{year}", response_model=List[Price])
def read_prices_by_year(year: int, db: Session = Depends(get_db)):
    """
    Retrieve Bitcoin price records for a specific year.
    """
    prices = get_price_by_year(db, year)
    if not prices:
        raise HTTPException(status_code=404, detail="Prices not found for the specified year")
    return prices

@router.get("/prices/halving/{halving_number}", response_model=List[Price])
def read_prices_by_halving(halving_number: int, db: Session = Depends(get_db)):
    """
    Retrieve Bitcoin price records for a specific halving period.
    """
    prices = get_prices_by_halving(db, halving_number)
    if not prices:
        raise HTTPException(status_code=404, detail="Prices not found for the specified halving period")
    return prices

@router.get("/prices/halvings", response_model=List[Price])
def read_prices_across_halvings(db: Session = Depends(get_db)):
    """
    Retrieve Bitcoin price records across all halving periods.
    """
    prices = get_prices_across_halvings(db)
    return prices

@router.get("/prices/bybit/", response_model=List[Price])
def read_bybit_prices(db: Session = Depends(get_db)):
    """
    Retrieve Bitcoin price records from Bybit.
    """
    prices = get_bybit_price()
    return prices

@router.get("/prices/binance/", response_model=List[Price])
def read_binance_prices(db: Session = Depends(get_db)):
    """
    Retrieve Bitcoin price records from Binance.
    """
    prices = get_binance_price()
    return prices

@router.get("/prices/kraken/", response_model=List[Price])
def read_kraken_prices(db: Session = Depends(get_db)):
    """
    Retrieve Bitcoin price records from Kraken.
    """
    prices = get_kraken_price()
    return prices

@router.get("/prices/yahoo/", response_model=List[Price])
def read_yahoo_prices(db: Session = Depends(get_db)):
    """
    Retrieve Bitcoin price records from Yahoo Finance.
    """
    prices = get_yahoo_price()
    return prices
