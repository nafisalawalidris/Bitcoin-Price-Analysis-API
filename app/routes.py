from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas
from .database import get_db

router = APIRouter()

@router.get("/prices/", response_model=List[schemas.BitcoinPriceRead])
def read_prices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_prices(db, skip=skip, limit=limit)

@router.get("/prices/{year}", response_model=List[schemas.BitcoinPriceRead])
def read_prices_by_year(year: int, db: Session = Depends(get_db)):
    prices = crud.get_prices_by_year(db, year)
    if not prices:
        raise HTTPException(status_code=404, detail="Prices not found for the specified year.")
    return prices

@router.get("/prices/halving/{halving_number}", response_model=List[schemas.BitcoinPriceRead])
def read_prices_by_halving(halving_number: int, db: Session = Depends(get_db)):
    prices = crud.get_prices_by_halving(db, halving_number)
    if not prices:
        raise HTTPException(status_code=404, detail="Prices not found for the specified halving number.")
    return prices

@router.get("/prices/halvings", response_model=List[schemas.BitcoinPriceRead])
def read_prices_across_halvings(db: Session = Depends(get_db)):
    return crud.get_prices_across_halvings(db)

@router.get("/prices/bybit")
def get_latest_bybit_price():
    return crud.get_bybit_prices()

@router.get("/prices/binance")
def get_latest_binance_price():
    return crud.get_binance_prices()

@router.get("/prices/kraken")
def get_latest_kraken_price():
    return crud.get_kraken_prices()

@router.get("/prices/yahoo")
def get_latest_yahoo_price():
    return crud.get_yahoo_prices()

@router.get("/prices/luno")
def get_latest_luno_price():
    return crud.get_luno_prices()

@router.get("/prices/remitano")
def get_latest_remitano_price():
    return crud.get_remitano_prices()

@router.get("/prices/kucoin")
def get_latest_kucoin_price():
    return crud.get_kucoin_prices()
