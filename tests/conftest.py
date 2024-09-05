import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import BitcoinPrice
from app.main import app
from app.database import get_db
from fastapi.testclient import TestClient

# Database configuration for tests
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    # Create a fresh database schema for each test function
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Insert sample data
    db = TestingSessionLocal()
    try:
        # Add sample Bitcoin prices
        sample_prices = [
            BitcoinPrice(date="2012-10-01", price=12.50),
            BitcoinPrice(date="2012-11-01", price=13.00),
            BitcoinPrice(date="2012-12-01", price=14.00),
            BitcoinPrice(date="2013-01-01", price=15.00),
            BitcoinPrice(date="2013-02-01", price=16.00),
        ]
        db.add_all(sample_prices)
        db.commit()
        
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    # Override the get_db dependency to use the test database session
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
