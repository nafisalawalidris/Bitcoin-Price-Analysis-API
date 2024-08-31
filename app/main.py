from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas
from .database import SessionLocal
from fastapi import FastAPI
from app.schemas import Price, PriceList

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/prices/", response_model=List[schemas.Price])
def get_all_prices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    prices = crud.get_prices(db, skip=skip, limit=limit)
    return prices

@app.get("/prices/{year}", response_model=List[schemas.Price])
def get_prices_by_year(year: int, db: Session = Depends(get_db)):
    prices = crud.get_prices_by_year(db, year=year)
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the given year")
    return prices

@app.get("/prices/halving/{halving_number}", response_model=List[schemas.Price])
def get_prices_by_halving(halving_number: int, db: Session = Depends(get_db)):
    prices = crud.get_prices_by_halving(db, halving_number=halving_number)
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the given halving period")
    return prices

@app.get("/prices/bybit")
def get_bybit_prices_endpoint():
    prices = crud.get_bybit_prices()
    return prices

@app.get("/prices/binance")
def get_binance_prices_endpoint():
    prices = crud.get_binance_prices()
    return prices

@app.get("/prices/kraken")
def get_kraken_prices_endpoint():
    prices = crud.get_kraken_prices()
    return prices

@app.get("/prices/yahoo")
def get_yahoo_prices_endpoint():
    prices = crud.get_yahoo_prices()
    return prices
