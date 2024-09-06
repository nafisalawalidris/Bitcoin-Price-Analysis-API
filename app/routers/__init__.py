from fastapi import FastAPI, Depends
from app.routes import bitcoin_price_router
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import logging
import os

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Database configuration
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/Bitcoin_Prices_Database')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI instance
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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bitcoin Price API. Please visit /api/0.1.0/prices/ for API endpoints."}

app.include_router(bitcoin_price_router, prefix="/api/0.1.0", tags=['bitcoin_prices'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    logging.info("Starting up the application.")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down the application.")
