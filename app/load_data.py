import pandas as pd
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import SessionLocal, engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)

def load_csv_to_db(csv_file: str):
    # Load data from CSV using pandas
    df = pd.read_csv(csv_file, parse_dates=['Date'])

    # Convert DataFrame to list of BitcoinPriceCreate schemas
    prices = [
        schemas.BitcoinPriceCreate(
            date=row['Date'],
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            adj_close=row['Adj Close'],
            volume=row['Volume']
        )
        for index, row in df.iterrows()
    ]

    # Insert data into the database
    db = SessionLocal()
    for price in prices:
        crud.create_price(db=db, price=price)
    db.close()

# Run the data load
load_csv_to_db('data/BTC-USD Yahoo Finance - Max Yrs.csv')
