from fastapi import FastAPI
from . import schemas, crud
from .database import engine
from typing import List

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

@app.get("/prices/", response_model=List[schemas.BitcoinPrice])
def get_all_prices(db: Depends(crud.get_db)):
    return crud.get_all_prices(db)

@app.get("/prices/{year}", response_model=List[schemas.BitcoinPrice])
def get_prices_by_year(year: int, db: Depends(crud.get_db)):
    return crud.get_prices_by_year(db, year)

@app.get("/prices/halving/{halving_number}", response_model=List[schemas.BitcoinPrice])
def get_prices_by_halving(halving_number: int, db: Depends(crud.get_db)):
    return crud.get_prices_by_halving(db, halving_number)

@app.get("/prices/halvings", response_model=List[schemas.BitcoinPrice])
def get_prices_across_halvings(db: Depends(crud.get_db)):
    return crud.get_prices_across_halvings(db)
