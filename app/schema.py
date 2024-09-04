import sys
import os
from sqlalchemy import create_engine
from app.models import Base  

# Add the 'app' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine

def create_schema():
    # Create all tables defined in the Base metadata
    Base.metadata.create_all(bind=engine)
    print("Database schema created successfully.")

if __name__ == "__main__":
    create_schema()
