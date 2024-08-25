from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, Column, Date, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import psycopg2
import asyncio  # Import asyncio

DATABASE_URL = "postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Float)

class BitcoinPriceBase(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

class BitcoinPriceResponse(BitcoinPriceBase):
    id: int

app = FastAPI()

async def load_data_to_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("Database connection was successful!")

        csv_file_path = "C:/Users/USER/Downloads/Bitcoin-Price-Analysis-API/data/BTC-USD Yahoo Finance - Max Yrs.csv"
        df = pd.read_csv(csv_file_path)
        df['Date'] = pd.to_datetime(df['Date'])

        cur.execute("""
            CREATE TABLE IF NOT EXISTS bitcoin_prices (
                id SERIAL PRIMARY KEY,
                date DATE,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                adj_close FLOAT,
                volume FLOAT
            )
        """)

        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO bitcoin_prices (date, open, high, low, close, adj_close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']))

        conn.commit()
        cur.close()
        conn.close()
        print("Data loaded successfully!")

    except Exception as error:
        print("An error occurred:", error)

@app.on_event("startup")
async def startup_event():
    # Run the data loading in a background task
    asyncio.create_task(load_data_to_db())

@app.on_event("shutdown")
async def shutdown_event():
    # Any cleanup code here
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/prices/{year}", response_model=List[BitcoinPriceResponse])
def get_prices_by_year(year: int, db: Session = Depends(get_db)):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    prices = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all()
    
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the given year")
    return prices

@app.get("/halving-prices/{number_of_halvings}", response_model=List[BitcoinPriceResponse])
def get_prices_by_halving(number_of_halvings: int, db: Session = Depends(get_db)):
    halving_periods = [
        (datetime(2012, 11, 28), datetime(2016, 7, 9)),
        (datetime(2016, 7, 9), datetime(2020, 5, 11)),
        (datetime(2020, 5, 11), datetime(2024, 3, 14)),
    ]
    
    if number_of_halvings < 1 or number_of_halvings > len(halving_periods):
        raise HTTPException(status_code=400, detail="Invalid number of halving periods")
    
    start_date, end_date = halving_periods[number_of_halvings - 1]
    prices = db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all()
    
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for the given halving period")
    return prices
