import sys
import os
import logging
from sqlalchemy import create_engine
from app.models import Base  # Ensure that Base is correctly defined in app.models
from app.database import engine  # Ensure that engine is correctly defined in app.database

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the 'app' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_schema():
    try:
        # Create all tables defined in the Base metadata
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema created successfully.")
    except Exception as e:
        logger.error(f"An error occurred while creating the database schema: {e}")

if __name__ == "__main__":
    create_schema()
