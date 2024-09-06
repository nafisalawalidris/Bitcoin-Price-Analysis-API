from pydantic import BaseModel
from typing import List
import sys
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from app.models import Base
from app.database import engine  # Ensure this is correctly imported
class Price(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int

class HalvingPricesResponse(BaseModel):
    halving_number: int
    prices: List[Price]

class StatisticsResponse(BaseModel):
    min_price: float
    max_price: float
    avg_price: float
    total_entries: int
    
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_schema():
    """Create all tables defined in the Base metadata."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema created successfully.")
    except SQLAlchemyError as e:
        logger.error(f"An error occurred while creating the database schema: {e}")
        logger.debug(e, exc_info=True)

if __name__ == "__main__":
    create_schema()


