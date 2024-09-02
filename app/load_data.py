import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
from models import BitcoinPrice, Base, engine

def load_csv_to_postgres(csv_file_path: str):
    # Read CSV file
    df = pd.read_csv(csv_file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')  # Convert to datetime
    df['Volume'] = df['Volume'].str.replace(',', '').astype(int)  # Convert volume to integer

    # Create database session
    session = SessionLocal()

    try:
        for index, row in df.iterrows():
            record = BitcoinPrice(
                date=row['Date'],
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                adj_close=row['Adj Close'],
                volume=row['Volume']
            )
            session.add(record)

        session.commit()
        print("Data committed successfully.")
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Path to your CSV file
    csv_file_path = "C:/Users/USER/Downloads/Bitcoin-Price-Analysis-API/data/BTC-USD Yahoo Finance - Max Yrs.csv"

    # Load data into PostgreSQL
    load_csv_to_postgres(csv_file_path)
