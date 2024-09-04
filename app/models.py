from sqlalchemy import Column, Numeric, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BitcoinPrice(Base):
    __tablename__ = 'bitcoin_prices'

    date = Column(DateTime, primary_key=True)  
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=False)
    volume = Column(Numeric, nullable=False)  

    def to_dict(self):
        return {
            "date": self.date.strftime('%Y-%m-%d'),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "adj_close": self.adj_close,
            "volume": float(self.volume)  
        }
