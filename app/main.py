from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine, Base

# Create FastAPI instance
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define endpoints here
@app.get("/")
def read_root():
    print("Successfully")
    return {"message": "Welcome to the Bitcoin Price API"}

@app.get("/root/")
def read_root_details():
    print("Successfully")
    return {
        "endpoints": {
            "/prices/": "Retrieves all historical Bitcoin prices",
            "/prices/{year}": "Fetches Bitcoin prices for a specific year",
            "/prices/halving/{halving_number}": "Provides Bitcoin price data around specific halving events",
            "/prices/halvings": "Retrieves Bitcoin prices across all halving periods"
        }
    }

@app.get("/prices/", response_model=List[schemas.BitcoinPrice])
def get_all_prices(db: Session = Depends(get_db)):
    print("All prices successfully fetched from Postgres database")
    return crud.get_all_prices(db=db)

@app.get("/prices/{year}", response_model=List[schemas.BitcoinPrice])
def get_prices(year: int, db: Session = Depends(get_db)):
    # Use the CRUD function to fetch prices by year
    prices = crud.get_prices_by_year(db=db, year=year)
    print("Successfully displayed bitcoin prices per year from 2014 to 2024 fetched from Postgres database")
    return prices

HALVING_DATES = {
    1: "2012-11-28",
    2: "2016-07-09",
    3: "2020-05-11",
    4: "2024-04-19"  
}

@app.get("/prices/halving/{halving_number}")
def get_prices_by_halving_endpoint(halving_number: int, db: Session = Depends(get_db)):
    if halving_number not in HALVING_DATES:
        raise HTTPException(status_code=404, detail="Halving number not found")
    
    try:
        prices = crud.get_prices_by_halving(db=db, halving_number=halving_number)
        print("Successfully displayed bitcoin prices by halving number from 2014 to 2024 fetched from Postgres database")
        return prices
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/prices/halvings", response_model=List[schemas.BitcoinPrice])
def get_prices_across_halvings(db: Session = Depends(get_db)):
    try:
        prices = crud.get_prices_across_halvings(db=db)
        print("Successfully displayed bitcoin prices across all the 4 halvings from 2014 to 2024 fetched from Postgres database")
        return prices
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
