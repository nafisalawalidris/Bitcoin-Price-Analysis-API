# load_data.py
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, BitcoinPrice
from database import engine, SessionLocal

# Load CSV file
csv_file_path = "C:/Users/USER/Downloads/Bitcoin-Price-Analysis-API/data/BTC-USD Yahoo Finance - Max Yrs.csv"

df = pd.read_csv(csv_file_path)

# Preprocess the data if necessary
df['Date'] = pd.to_datetime(df['Date'])
df.columns = [col.lower().replace(' ', '_') for col in df.columns]

# Create tables
Base.metadata.create_all(bind=engine)

# Load data into PostgreSQL
def load_data():
    session = SessionLocal()
    try:
        df.to_sql('bitcoin_prices', con=engine, if_exists='append', index=False)
    finally:
        session.close()

if __name__ == "__main__":
    load_data()
