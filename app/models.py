from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL, replace with your actual database credentials
DATABASE_URL = "postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the models
Base = declarative_base()

# Define the BitcoinPrice model
class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"
    __table_args__ = {'extend_existing': True}  # Add this line

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

