from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
from datetime import date
import pandas as pd

# Define the SQLAlchemy database URL - this should match your PostgreSQL connection details
DATABASE_URL = "postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database"

# Set up the SQLAlchemy database engine
engine = create_engine(DATABASE_URL)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare the Base class for SQLAlchemy models to inherit from
Base = declarative_base()

# Define the SQLAlchemy model for the bitcoin_prices table
class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, unique=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Float)

# Pydantic schema for data validation
class BitcoinPriceBase(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

class BitcoinPriceResponse(BitcoinPriceBase):
    id: int

    class Config:
        orm_mode = True

# Initialise the FastAPI application
app = FastAPI()

# Dependency function to create a new database session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoint to retrieve all Bitcoin price entries
@app.get("/prices/", response_model=List[BitcoinPriceResponse])
def get_all_prices(db: Session = Depends(get_db)):
    prices = db.query(BitcoinPrice).all()
    return prices

# API endpoint to get Bitcoin price entries for a specific year
@app.get("/prices/{year}", response_model=List[BitcoinPriceResponse])
def get_prices_by_year(year: int, db: Session = Depends(get_db)):
    if year < 0:
        raise HTTPException(status_code=400, detail="Invalid year")
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    prices = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all()
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the given year")
    return prices

# API endpoint to get Bitcoin price entries for a specific halving period
@app.get("/prices/halving/{halving_number}", response_model=List[BitcoinPriceResponse])
def get_prices_by_halving(halving_number: int, db: Session = Depends(get_db)):
    # Define halving dates (approximate dates for halving events)
    halving_dates = {
        1: "2012-11-28",
        2: "2016-07-09",
        3: "2020-05-11",
        4: "2024-04-20",
    }
    
    if halving_number not in halving_dates:
        raise HTTPException(status_code=404, detail="Halving period not found")
    
    start_date = halving_dates[halving_number]
    end_date = pd.to_datetime(start_date) + pd.DateOffset(years=4)
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    prices = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date_str)).all()
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the given halving period")
    return prices

# API endpoint to get Bitcoin price entries across all halving periods
@app.get("/prices/halvings", response_model=List[BitcoinPriceResponse])
def get_prices_across_halvings(db: Session = Depends(get_db)):
    # Define halving dates
    halving_dates = [
        "2012-11-28",
        "2016-07-09",
        "2020-05-11",
        "2024-04-20"
    ]
    
    prices = []
    for start_date in halving_dates:
        end_date = pd.to_datetime(start_date) + pd.DateOffset(years=4)
        end_date_str = end_date.strftime("%Y-%m-%d")
        prices.extend(db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date_str)).all())
    
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the halving periods")
    return prices
