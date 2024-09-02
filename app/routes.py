from fastapi import APIRouter, Depends
from typing import List
from . import schemas, crud

router = APIRouter()

@router.get("/", response_model=dict)
def read_root():
    return {
        "message": "Welcome to the Bitcoin Price Analysis API!",
        "endpoints": {
            "/prices/": "Retrieve all historical Bitcoin prices.",
            "/prices/{year}": "Fetch Bitcoin prices for a specific year.",
            "/prices/halving/{halving_number}": "Obtain Bitcoin prices around specific Bitcoin halving events.",
            "/prices/halvings": "Retrieve Bitcoin prices across all halving periods."
        }
    }

@router.get("/prices/", response_model=List[schemas.BitcoinPrice])
def get_all_prices(db: Depends(crud.get_db)):
    return crud.get_all_prices(db)

@router.get("/prices/{year}", response_model=List[schemas.BitcoinPrice])
def get_prices_by_year(year: int, db: Depends(crud.get_db)):
    return crud.get_prices_by_year(db, year)

@router.get("/prices/halving/{halving_number}", response_model=List[schemas.BitcoinPrice])
def get_prices_by_halving(halving_number: int, db: Depends(crud.get_db)):
    return crud.get_prices_by_halving(db, halving_number)

@router.get("/prices/halvings", response_model=List[schemas.BitcoinPrice])
def get_prices_across_halvings(db: Depends(crud.get_db)):
    return crud.get_prices_across_halvings(db)
