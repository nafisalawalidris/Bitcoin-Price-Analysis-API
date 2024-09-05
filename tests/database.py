import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings  # Ensure this import is correct
from app.database import get_db, Base

# Define the test database URL using settings
SQLALCHEMY_TEST_DATABASE_URL = (
    f'postgresql://{settings.database_username}:'
    f'{settings.database_password}@'
    f'{settings.database_hostname}:'
    f'{settings.database_port}/'
    f'{settings.test_database_name}'
)

# Create the SQLAlchemy engine for the test database
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

# Create a session local for testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    # Drop all tables and create new ones for each test function
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
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
