import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings  # Import settings from config file
from app.routers import historical, real_time  # Import routers for different functionalities
from app.database import Base  # Import the Base class for ORM

# Create FastAPI instance
app = FastAPI()

# Database configuration using settings
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}@"
    f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# Create the SQLAlchemy engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include routers for better modularity
app.include_router(historical.router, prefix="/historical", tags=["Historical Data"])
app.include_router(real_time.router, prefix="/real-time", tags=["Real-Time Data"])

# Event handler to create database tables on startup (if necessary)
@app.on_event("startup")
def startup_event():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)

# Event handler to run cleanup tasks on shutdown
@app.on_event("shutdown")
def shutdown_event():
    # Add any necessary cleanup logic here
    pass

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Bitcoin Price Analysis and Real-Time Data API"}

# Main entry point for running the app
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
