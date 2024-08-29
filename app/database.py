from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pandas as pd
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connection string using environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Feenah413")  # Default password if not set in .env
POSTGRES_DB = os.getenv("POSTGRES_DB", "Bitcoin_Prices_Database")
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB}"

# Create the SQLAlchemy engine
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    logger.info("Database engine created successfully.")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Configure the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Function to load data from CSV to PostgreSQL
def load_csv_to_postgresql(csv_file_path: str, table_name: str):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Print DataFrame to check contents
        logger.info(f"DataFrame head:\n{df.head()}")
        
        # Load DataFrame into the PostgreSQL table
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        logger.info(f"Data from {csv_file_path} has been loaded into the table {table_name} successfully.")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

# Test the database connection
def test_connection():
    try:
        with engine.connect() as connection:
            logger.info("Connected to the database successfully.")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise

# Call the test_connection function to check the connection
test_connection()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test reading the CSV file
csv_file_path = r"C:\Users\USER\Downloads\Bitcoin-Price-Analysis-API\data\BTC-USD Yahoo Finance - Max Yrs.csv"
try:
    df = pd.read_csv(csv_file_path)
    print(df.head())
except Exception as e:
    print(f"Failed to read CSV file: {e}")

# Load CSV data into PostgreSQL
load_csv_to_postgresql(csv_file_path, 'bitcoin_prices')
