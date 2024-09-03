from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import engine, SessionLocal, Base

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/root/")
def read_root():
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
    return crud.get_all_prices(db=db)

@app.get("/prices/{year}", response_model=List[schemas.BitcoinPrice])
def get_prices_by_year(year: int, db: Session = Depends(get_db)):
    return crud.get_prices_by_year(db=db, year=year)

@app.get("/prices/halving/{halving_number}", response_model=List[schemas.BitcoinPrice])
def get_prices_by_halving(halving_number: int, db: Session = Depends(get_db)):
    return crud.get_prices_by_halving(db=db, halving_number=halving_number)

@app.get("/prices/halvings", response_model=List[schemas.BitcoinPrice])
def get_prices_across_halvings(db: Session = Depends(get_db)):
    return crud.get_prices_across_halvings(db=db)
