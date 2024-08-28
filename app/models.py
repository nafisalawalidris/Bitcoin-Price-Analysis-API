from sqlalchemy import Column, Integer, Float, Date
from .database import Base
from pydantic import BaseModel
from datetime import date


# Define a SQLAlchemy model for Bitcoin price data
class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"

    id = Column(Integer, primary_key=True, nullable=False)  
    date = Column(Date, nullable=False)  
    open = Column(Float, nullable=False)  
    high = Column(Float, nullable=False)  
    low = Column(Float, nullable=False)  
    close = Column(Float, nullable=False)  
    adj_close = Column(Float, nullable=False) 
    volume = Column(Float, nullable=False)  


# Define Pydantic models for Bitcoin price data
class BitcoinPriceBase(BaseModel):
    date: date  
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float


class BitcoinPriceCreate(BitcoinPriceBase):
    pass


class BitcoinPriceResponse(BitcoinPriceBase):
    id: int

    class Config:
        orm_mode = True
