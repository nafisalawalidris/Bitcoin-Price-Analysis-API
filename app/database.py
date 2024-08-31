# Import necessary libraries from SQLAlchemy
from sqlalchemy import create_engine, Column, Date, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Define the database URL.
# Replace 'username', 'password', 'localhost', and 'dbname' with your PostgreSQL credentials.
DATABASE_URL = "postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database"

# Create the SQLAlchemy engine.
# The engine is responsible for connecting to the database and executing SQL commands.
# We use 'create_engine' to initialize the connection to the PostgreSQL database.
engine = create_engine(DATABASE_URL, echo=True)  # echo=True logs all the SQL commands

# Create a SessionLocal class that will serve as a factory for creating new Session objects.
# Sessions are used to interact with the database and perform CRUD operations.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models.
# All model classes will inherit from this base class.
# The base class is used to create the database schema and manage the metadata.
Base = declarative_base()

# Dependency for getting a database session.
# This function will be used in FastAPI endpoints to get a session for interacting with the database.
def get_db():
    # Create a new session.
    db = SessionLocal()
    try:
        # Yield the session object to be used in the request.
        yield db
    finally:
        # Close the session when done.
        db.close()

# Load the dataset from a CSV file
# Use raw string (r'path') or double backslashes for Windows paths
df = pd.read_csv(r"C:\Users\USER\Downloads\Bitcoin-Price-Analysis-API\data\BTC-USD Yahoo Finance - Max Yrs.csv", parse_dates=['Date'])

# Check for missing values
print(df.isnull().sum())

# Drop rows with missing values (if necessary)
df = df.dropna()

# Convert columns to appropriate data types
df['Date'] = pd.to_datetime(df['Date'])  # Ensure 'Date' is in datetime format
df['Volume'] = df['Volume'].astype(int)  # Convert 'Volume' to integer

class BitcoinPrice(Base):
    __tablename__ = 'bitcoin_prices'
    
    date = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Integer)

# Create the table
Base.metadata.create_all(bind=engine)

def insert_data(df):
    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            price = BitcoinPrice(
                date=row['Date'],
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                adj_close=row['Adj Close'],
                volume=row['Volume']
            )
            session.add(price)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

# Insert the data
insert_data(df)
