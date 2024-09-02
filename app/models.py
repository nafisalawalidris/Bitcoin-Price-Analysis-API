from sqlalchemy import Column, Integer, Float, Date
from .database import Base

class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    date = Column(Date, index=True)  # Date of the price
    open = Column(Float)  # Opening price
    high = Column(Float)  # Highest price of the day
    low = Column(Float)  # Lowest price of the day
    close = Column(Float)  # Closing price
    volume = Column(Float)  # Volume of Bitcoin traded
    market_cap = Column(Float)  # Market capitalization

    def __repr__(self):
        return f"<BitcoinPrice(id={self.id}, date={self.date}, open={self.open}, high={self.high}, low={self.low}, close={self.close}, volume={self.volume}, market_cap={self.market_cap})>"
