from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os
import logging
from datetime import date
from sqlalchemy import Column, Float, Date, Index

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connection string using environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Feenah413")  # Default password if not set in .env
POSTGRES_DB = os.getenv("POSTGRES_DB", "Bitcoin_Prices_Database")
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database"

# Create the SQLAlchemy engine
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    logger.info("Database engine created successfully.")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Base class for declarative models
Base = declarative_base()

# Define a SQLAlchemy model for Bitcoin price data
class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"

    date = Column(Date, primary_key=True, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    # Example of creating an index on 'date' for faster queries
    __table_args__ = (
        Index('ix_date', 'date'),
    )

# Create the table in the database
Base.metadata.create_all(bind=engine)

# Configure the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_csv_to_postgresql(csv_file_path: str, table_name: str):
    """
    Load a CSV file into a PostgreSQL table.
    
    Parameters:
    csv_file_path (str): Path to the CSV file.
    table_name (str): Name of the table in the PostgreSQL database.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Print DataFrame to check contents
        logger.info(f"DataFrame head:\n{df.head()}")
        
        # Load data to PostgreSQL
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logger.info(f"Data from {csv_file_path} has been loaded into the table {table_name} successfully.")
    except Exception as e:
        logger.error(f"Error loading CSV data to PostgreSQL: {e}")
        raise

def test_connection():
    """
    Test the connection to the PostgreSQL database.
    """
    try:
        with engine.connect() as connection:
            logger.info("Connected to the database successfully.")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise

if __name__ == "__main__":
    # Test the database connection
    test_connection()
    
    # Path to CSV file
    csv_file_path = r"C:\Users\USER\Downloads\Bitcoin-Price-Analysis-API\data\BTC-USD Yahoo Finance - Max Yrs.csv"
    
    # Load CSV data into PostgreSQL
    load_csv_to_postgresql(csv_file_path, 'bitcoin_prices')

    # Create a new session for querying
    db = SessionLocal()

    try:
        # Query the database to ensure data was inserted
        bitcoin_prices = db.query(BitcoinPrice).all()
        print(bitcoin_prices)
    except Exception as e:
        logger.error(f"Error querying data from PostgreSQL: {e}")
    finally:
        # Close the session
        db.close()
