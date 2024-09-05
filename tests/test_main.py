import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from app.models import BitcoinPrice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database configuration for tests
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    # Setup database schema
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
    # Override the dependency to use the test database session
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Bitcoin Price API"}

def test_read_root_details(client):
    response = client.get("/root/")
    assert response.status_code == 200
    assert response.json() == {
        "overview": "This API provides various endpoints to access historical Bitcoin price data.",
        "endpoints": {
            "/prices/": "Retrieves all historical Bitcoin prices",
            "/prices/{year}": "Fetches Bitcoin prices for a specific year",
            "/prices/halving/{halving_number}": "Provides Bitcoin price data around specific halving events",
            "/prices/halvings": "Retrieves Bitcoin prices across all halving periods"
        }
    }

def test_get_all_prices(client):
    response = client.get("/prices/")
    assert response.status_code == 200
    assert isinstance(response.json()["prices"], list)

def test_get_prices_by_year(client):
    # Test for a year with expected data
    response = client.get("/prices/2012")
    assert response.status_code == 200
    assert isinstance(response.json()["prices"], list)

    # Test for a year with no data
    response = client.get("/prices/1900")
    assert response.status_code == 404

def test_read_prices_around_halving(client):
    response = client.get("/prices/halving/1")
    assert response.status_code == 200
    data = response.json()
    assert "halving_number" in data
    assert data["halving_number"] == 1
    assert "prices" in data
    assert isinstance(data["prices"], list)
    assert len(data["prices"]) > 0  # Ensure some data is returned
