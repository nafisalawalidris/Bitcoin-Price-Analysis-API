from sqlalchemy import Column, Float, Date, Index
from .database import Base
from pydantic import BaseModel, validator
from datetime import date

# Define a SQLAlchemy model for Bitcoin price data
class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"

    date = Column(Date, primary_key=True, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    # Example of creating an index on 'date' for faster queries
    __table_args__ = (
        Index('ix_date', 'date'),
    )

# Define Pydantic models for Bitcoin price data
class BitcoinPriceBase(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

    @validator('volume')
    def check_volume_positive(cls, v):
        if v < 0:
            raise ValueError('Volume must be positive')
        return v

class BitcoinPriceCreate(BitcoinPriceBase):
    pass

class BitcoinPriceResponse(BitcoinPriceBase):
    id: int

    class Config:
        orm_mode = True
