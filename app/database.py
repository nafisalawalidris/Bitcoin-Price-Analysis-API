from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# SQLAlchemy engine creation
engine = create_engine(DATABASE_URL)

# Session creation for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency function for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
