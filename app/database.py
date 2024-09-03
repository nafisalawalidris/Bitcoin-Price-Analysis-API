from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import psycopg2

# Define the database URL
DATABASE_URL = "postgresql://postgres:Feenah413@localhost/Bitcoin_Prices_Database"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to load data into PostgreSQL
def load_data_into_postgres(file_path: str):
    # Read and transform data
    df = pd.read_csv(file_path)
    df = df.dropna()
    df = df.rename(columns={'tpep_pickup_datetime': 'pickup_datetime', 'tpep_dropoff_datetime': 'dropoff_datetime'})
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])
    df['trip_duration'] = df['dropoff_datetime'] - df['pickup_datetime']
    df['trip_duration_minutes'] = df['trip_duration'].dt.total_seconds() / 60

    # Connect to PostgreSQL and create the table if needed
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS bitcoin_prices (
                id SERIAL PRIMARY KEY,
                date TIMESTAMP,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                adj_close FLOAT,
                volume FLOAT
            );
            """)
            conn.commit()

    # Load data into PostgreSQL
    try:
        df.to_sql('bitcoin_prices', engine, if_exists='replace', index=False)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Data loading failed: {e}")
