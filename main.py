# main.py

from fastapi import FastAPI, HTTPException, Depends  # FastAPI and its components for creating the API and handling errors
from sqlalchemy import create_engine, Column, Integer, Float, Date  # SQLAlchemy for database operations and defining columns
from sqlalchemy.ext.declarative import declarative_base  # Base class for SQLAlchemy models
from sqlalchemy.orm import sessionmaker, Session  # ORM tools to create and manage database sessions
from pydantic import BaseModel  # Pydantic for data validation and schema creation
from typing import List  # Typing module to specify list types in function definitions
import asyncio  # Asyncio for running asynchronous functions (e.g., loading data on startup)
import pandas as pd  # Pandas for data manipulation (used here to read CSV files)
import os  # OS module to handle environment variables and file paths

# Define the SQLAlchemy database URL - this should match your PostgreSQL connection details
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database")

# Set up the SQLAlchemy database engine
engine = create_engine(DATABASE_URL)

# Create a session maker, which generates new Session objects when called
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare the Base class for SQLAlchemy models to inherit from
Base = declarative_base()

# Define the SQLAlchemy model for the bitcoin_prices table
class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column (auto-incrementing)
    date = Column(Date, index=True, unique=True)  # Date of the Bitcoin price entry, must be unique to avoid duplicates
    open = Column(Float)  # Opening price of Bitcoin on the date
    high = Column(Float)  # Highest price of Bitcoin on the date
    low = Column(Float)  # Lowest price of Bitcoin on the date
    close = Column(Float)  # Closing price of Bitcoin on the date
    adj_close = Column(Float)  # Adjusted closing price of Bitcoin on the date
    volume = Column(Float)  # Trading volume of Bitcoin on the date

# Pydantic schema for data validation
class BitcoinPriceBase(BaseModel):
    date: str  # The date of the price entry as a string
    open: float  # The opening price
    high: float  # The highest price
    low: float  # The lowest price
    close: float  # The closing price
    adj_close: float  # The adjusted closing price
    volume: float  # The trading volume

# Pydantic schema for creating a new Bitcoin price entry
class BitcoinPriceCreate(BitcoinPriceBase):
    pass  # Inherits all fields from BitcoinPriceBase without changes

# Pydantic schema for response data, including an ID
class BitcoinPriceResponse(BitcoinPriceBase):
    id: int  # ID of the price entry

    class Config:
        orm_mode = True  # Enable ORM mode to work with SQLAlchemy models

# Initialize the FastAPI application
app = FastAPI()

# Dependency function to create a new database session per request
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session object to be used in API endpoints
    finally:
        db.close()  # Close the session after the request is finished

# Create the database tables (if they do not exist) when the application starts
Base.metadata.create_all(bind=engine)

# Asynchronous function to load CSV data into the database
async def load_data_to_db():
    try:
        with engine.connect() as connection:  # Create a raw connection to the database
            # Load CSV data into a Pandas DataFrame
            csv_file_path = "data\BTC-USD Yahoo Finance - Max Yrs.csv"
            df = pd.read_csv(csv_file_path)
            df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime

            # Iterate through DataFrame rows and insert each row into the database
            for _, row in df.iterrows():
                stmt = BitcoinPrice.__table__.insert().values(
                    date=row['Date'],
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    adj_close=row['Adj Close'],
                    volume=row['Volume']
                )
                connection.execute(stmt)  # Execute the insert statement for each row
            connection.commit()  # Commit all the transactions
            print("Data loaded successfully!")  # Log success message
    except Exception as error:
        print(f"An error occurred while loading data: {error}")  # Log error message

# Register an event to run the data loading function on application startup
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(load_data_to_db())  # Run load_data_to_db asynchronously

# API endpoint to retrieve all Bitcoin price entries
@app.get("/prices/", response_model=List[BitcoinPriceResponse])
def get_all_prices(db: Session = Depends(get_db)):
    """
    Retrieve all Bitcoin prices from the database.
    """
    prices = db.query(BitcoinPrice).all()  # Query all rows in the BitcoinPrice table
    return prices  # Return the results as a list

# API endpoint to add a new Bitcoin price entry
@app.post("/prices/", response_model=BitcoinPriceResponse)
def create_price(price: BitcoinPriceCreate, db: Session = Depends(get_db)):
    """
    Add a new Bitcoin price entry to the database.
    """
    db_price = BitcoinPrice(**price.dict())  # Create a new BitcoinPrice object from the input data
    db.add(db_price)  # Add the new object to the session
    db.commit()  # Commit the transaction to save the new entry in the database
    db.refresh(db_price)  # Refresh the session to reflect the saved entry
    return db_price  # Return the newly created entry
