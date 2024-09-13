from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os
import uvicorn
from app.routers import real_time
from app.routers.historical import bitcoin_price_router
from app.database import Base
from app.routers.real_time import real_time_router

# FastAPI instance with metadata
app = FastAPI(
    title="Bitcoin Price Analysis and Real-Time Data API",
    version="0.1.0",
    description=(  # Description updated for clarity
        "The Bitcoin Price Analysis and Real-Time Data API is an open-source API project designed to provide "
        "accurate, up-to-date and comprehensive Bitcoin pricing data for developers, researchers and financial "
        "analysts. Built on the robust FastAPI framework, this API offers seamless integration and high-performance "
        "endpoints for users who require real-time and historical Bitcoin price information. With Bitcoin being one of "
        "the most volatile and widely traded digital assets, access to reliable price data is critical for informed "
        "decision-making in trading, investment and market analysis. This API serves as a one-stop solution delivering "
        "data in a highly organised format that is easy to consume and use in various applications."
    ),
    contact={  # Contact details updated for clarity
        "name": "Nafisa Lawal Idris",
        "url": "https://nafisalawalidris.github.io/13/"
    },
    license_info={  # License information updated
        "name": "MIT",
    },
)

# Root Endpoint
@app.get("/", summary="Root Endpoint")
def root():
    return {
        "message": "Welcome to the Bitcoin Price Analysis and Real-Time Data API",
        "details": "Visit /api/0.1.0/root/ for information about the API endpoints and their descriptions."
    }

# Root Details
@app.get("/api/0.1.0/root/", tags=["Root"], summary="Root Details")
def read_root_details():
    return {
        "overview": "This API provides various endpoints to access historical Bitcoin price data.",
        "endpoints": [
            {
                "path": "/",
                "description": "Provides a welcome message and overview of the API."
            },
            {
                "path": "/api/0.1.0/root/",
                "description": "Provides information about the root of the API, including available endpoints and their descriptions."
            },
            {
                "path": "/historical/prices/",
                "description": "Retrieve the complete historical dataset of Bitcoin prices."
            },
            {
                "path": "/historical/prices/{year}",
                "description": "Fetch Bitcoin price data for a specific year."
            },
            {
                "path": "/historical/prices/halving/{halving_number}",
                "description": "Provide Bitcoin price data around a specific halving event."
            },
            {
                "path": "/historical/prices/statistics",
                "description": "Retrieve various statistical insights about Bitcoin prices over a specified period."
            },
            {
                "path": "/api/coingecko",
                "description": "Fetch Bitcoin price from CoinGecko.",
                "method": "GET"
            },
            {
                "path": "/api/coincap",
                "description": "Fetch Bitcoin price from CoinCap.",
                "method": "GET"
            },
            {
                "path": "/api/binance",
                "description": "Fetch Bitcoin price from Binance.",
                "method": "GET"
            },
            {
                "path": "/api/kraken",
                "description": "Fetch Bitcoin price from Kraken.",
                "method": "GET"
            }
        ]
    }

# Include routers for different functionalities
app.include_router(bitcoin_price_router, prefix="/historical", tags=["Historical Data"])
app.include_router(real_time_router, prefix="/api", tags=["Real-Time Data"])

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Database configuration
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

# Main entry point for running the app
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
