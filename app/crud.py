from sqlalchemy.orm import Session
from .models import BitcoinPrice
import requests

def get_prices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(BitcoinPrice).offset(skip).limit(limit).all()

def get_prices_by_year(db: Session, year: int):
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'
    return db.query(BitcoinPrice).filter(BitcoinPrice.date.between(start_date, end_date)).all()

def get_prices_by_halving(db: Session, halving_number: int):
    halving_periods = {
        1: ('2012-11-28', '2016-07-09'),
        2: ('2016-07-10', '2020-05-11'),
        3: ('2020-05-12', '2024-04-30'),
        4: ('2024-05-01', '2099-12-31')  # Assumes the fourth period extends to a future date
    }
    
    start_date, end_date = halving_periods.get(halving_number, (None, None))
    
    if start_date is None or end_date is None:
        return []  # Consider raising an HTTPException or returning an appropriate error message
    
    return db.query(BitcoinPrice).filter(
        BitcoinPrice.date >= start_date,
        BitcoinPrice.date <= end_date
    ).all()

def get_prices_across_halvings(db: Session):
    return db.query(BitcoinPrice).all()

def get_bybit_prices():
    try:
        response = requests.get('https://api.bybit.com/v2/public/tickers')
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        return data.get('result', [])
    except requests.RequestException as e:
        # Log the error or handle it as needed
        return {"error": str(e)}

def get_binance_prices():
    try:
        response = requests.get('https://api.binance.com/api/v3/ticker/price')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def get_kraken_prices():
    try:
        response = requests.get('https://api.kraken.com/0/public/Ticker')
        response.raise_for_status()
        data = response.json()
        return data.get('result', {})
    except requests.RequestException as e:
        return {"error": str(e)}

def get_yahoo_prices():
    try:
        response = requests.get('https://query1.finance.yahoo.com/v7/finance/quote?symbols=BTC-USD')
        response.raise_for_status()
        data = response.json()
        return data.get('quoteResponse', {}).get('result', [])
    except requests.RequestException as e:
        return {"error": str(e)}
