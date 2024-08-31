from sqlalchemy import Column, Float, Date, Index
from sqlalchemy.ext.declarative import declarative_base
from .database import Base  # Import Base from your database setup file

Base = declarative_base()

# Define a SQLAlchemy model for Bitcoin price data
class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"

    date = Column(Date, primary_key=True, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)  # Consider Integer if volume is always a whole number

    # Creating an index on 'date' for faster queries
    __table_args__ = (
        Index('ix_date', 'date'),
    )

    def __repr__(self):
        return (f"<BitcoinPrice(date={self.date}, open={self.open}, high={self.high}, "
                f"low={self.low}, close={self.close}, adj_close={self.adj_close}, volume={self.volume})>")
