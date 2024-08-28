from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connection string using environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database"

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
