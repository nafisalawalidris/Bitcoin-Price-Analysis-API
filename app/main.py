from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os
import uvicorn
from app.routers import historical, real_time
from app.database import Base

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# FastAPI instance with metadata
app = FastAPI(
    title="Bitcoin Price Analysis and Real-Time Data API",
    version="0.1.0",
    description=(
        "The Bitcoin Price Analysis and Real-Time Data API is an open-source API project designed to provide "
        "accurate, up-to-date and comprehensive Bitcoin pricing data for developers, researchers and financial "
        "analysts. Built on the robust FastAPI framework, this API offers seamless integration and high-performance "
        "endpoints for users who require real-time and historical Bitcoin price information. With Bitcoin being one of "
        "the most volatile and widely traded digital assets, access to reliable price data is critical for informed "
        "decision-making in trading, investment and market analysis. This API serves as a one-stop solution, delivering "
        "data in a highly organised format that is easy to consume and use in various applications."
    ),
    contact={
        "name": "Nafisa Lawal Idris",
        "portfolio": "https://nafisalawalidris.github.io/13/",
    },
    license_info={
        "name": "MIT",
    },
)

# Database configuration
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/Bitcoin_Prices_Database')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include routers for different functionalities
app.include_router(historical.router, prefix="/historical", tags=["Historical Data"])
app.include_router(real_time.router, prefix="/real-time", tags=["Real-Time Data"])

# Event handler to create database tables on startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    logging.info("Starting up the application.")

# Event handler to run cleanup tasks on shutdown
@app.on_event("shutdown")
def shutdown_event():
    logging.info("Shutting down the application.")
    # Add any necessary cleanup logic here

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Bitcoin Price Analysis and Real-Time Data API"}

# Main entry point for running the app
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
