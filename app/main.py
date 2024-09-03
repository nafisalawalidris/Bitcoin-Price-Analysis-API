from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import engine, get_db

# Create the FastAPI instance
app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    """
    Root endpoint that provides an overview of the API.

    Returns:
    - Dictionary with a welcome message and overview of available endpoints.
    """
    return {
        "message": "Welcome to the Bitcoin Price Analysis API!",
        "endpoints": {
            "/prices/": "Retrieve all historical Bitcoin prices.",
            "/prices/{year}": "Fetch Bitcoin prices for a specified year.",
            "/prices/halving/{halving_number}": "Get Bitcoin prices around specific halving events.",
            "/prices/halvings": "Retrieve Bitcoin prices across all halving periods.",
        }
    }

@app.get("/prices/", response_model=List[schemas.BitcoinPrice])
def read_all_prices(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all historical Bitcoin prices.

    Args:
    - db (Session): The SQLAlchemy database session.

    Returns:
    - List of BitcoinPrice objects representing all historical prices.
    """
    prices = crud.get_all_prices(db)
    return prices

@app.get("/prices/{year}", response_model=List[schemas.BitcoinPrice])
def read_prices_by_year(year: int, db: Session = Depends(get_db)):
    """
    Endpoint to fetch Bitcoin prices for a specific year.

    Args:
    - year (int): The year for which to fetch prices.
    - db (Session): The SQLAlchemy database session.

    Returns:
    - List of BitcoinPrice objects representing prices for the specified year.
    """
    prices = crud.get_prices_by_year(db, year)
    if not prices:
        raise HTTPException(status_code=404, detail="Prices not found for the given year")
    return prices

@app.get("/prices/halving/{halving_number}", response_model=List[schemas.BitcoinPrice])
def read_prices_by_halving(halving_number: int, db: Session = Depends(get_db)):
    """
    Endpoint to get Bitcoin prices around specific halving events.

    Args:
    - halving_number (int): The halving event number (e.g., 1, 2, 3, etc.).
    - db (Session): The SQLAlchemy database session.

    Returns:
    - List of BitcoinPrice objects representing prices around the specified halving event.
    """
    prices = crud.get_prices_by_halving(db, halving_number)
    if not prices:
        raise HTTPException(status_code=404, detail="Prices not found for the specified halving event")
    return prices

@app.get("/prices/halvings", response_model=List[schemas.BitcoinPrice])
def read_prices_across_halvings(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve Bitcoin prices across all halving periods.

    Args:
    - db (Session): The SQLAlchemy database session.

    Returns:
    - List of BitcoinPrice objects representing prices across all halving periods.
    """
    prices = crud.get_prices_across_halvings(db)
    return prices
