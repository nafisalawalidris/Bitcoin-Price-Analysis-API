from sqlalchemy import Column, Date, Float, Integer
from app.database import Base
from pydantic import BaseModel
from typing import Optional

class BitcoinPrice(Base):
    __tablename__ = 'bitcoin_prices'

    date = Column(Date, primary_key=True, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=True)
    volume = Column(Integer, nullable=False)

    def to_dict(self):
        """
        Converts the BitcoinPrice instance into a dictionary.
        """
        return {
            "date": self.date.strftime('%Y-%m-%d') if self.date else None,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "adj_close": self.adj_close,
            "volume": self.volume
        }

class BitcoinPriceResponse(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: Optional[float] = None
    volume: int
