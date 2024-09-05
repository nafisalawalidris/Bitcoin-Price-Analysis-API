from sqlalchemy import Column, Date, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BitcoinPrice(Base):
    __tablename__ = 'bitcoin_prices'

    date = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Integer)

    def to_dict(self):
        return {
            "date": self.date.strftime('%Y-%m-%d'),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "adj_close": self.adj_close,
            "volume": self.volume
        }

from pydantic import BaseModel
from typing import List, Optional

class Price(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int

class HalvingPricesResponse(BaseModel):
    halving_number: int
    prices: List[Price]