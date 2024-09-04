import pandas as pd
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models import BitcoinPrice
from sqlalchemy import insert

# Load CSV data
csv_file_path = "C:\\Users\\USER\\Downloads\\Bitcoin-Price-Analysis-API\\data\\BTC-USD Yahoo Finance - Max Yrs.csv"
data = pd.read_csv(csv_file_path)

# Convert scientific notation in the 'Volume' column to integers
data['Volume'] = data['Volume'].apply(lambda x: int(float(x)))

# Set up the database connection
Session = sessionmaker(bind=engine)
session = Session()

def load_data():
    for _, row in data.iterrows():
        # Prepare the data for insertion
        bitcoin_data = BitcoinPrice(
            date=pd.to_datetime(row['Date']).date(),
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            adj_close=row['Adj Close'],
            volume=row['Volume']
        )
        session.add(bitcoin_data)

    # Commit the changes to the database
    session.commit()
    print("Data loaded successfully into the table 'bitcoin_prices'.")

if __name__ == "__main__":
    load_data()
