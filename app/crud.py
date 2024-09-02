from sqlalchemy.orm import Session
from . import models, schemas

def get_prices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.BitcoinPrice).offset(skip).limit(limit).all()

def get_prices_by_year(db: Session, year: int):
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'
    return db.query(models.BitcoinPrice).filter(models.BitcoinPrice.date.between(start_date, end_date)).all()

def get_prices_by_halving(db: Session, halving_number: int):
    halving_periods = {
        1: ('2012-11-28', '2016-07-09'),
        2: ('2016-07-10', '2020-05-11'),
        3: ('2020-05-12', '2024-04-30'),
        4: ('2024-05-01', '2099-12-31')  # Future period assumption
    }
    
    start_date, end_date = halving_periods.get(halving_number, (None, None))
    
    if start_date is None or end_date is None:
        return []  # Consider returning an appropriate error message
    
    return db.query(models.BitcoinPrice).filter(
        models.BitcoinPrice.date >= start_date,
        models.BitcoinPrice.date <= end_date
    ).all()

def get_prices_across_halvings(db: Session):
    return db.query(models.BitcoinPrice).all()

def get_bybit_prices():
    # Function to fetch the latest price from Bybit API
    try:
        response = requests.get('https://api.bybit.com/v2/public/tickers')
        response.raise_for_status()
        data = response.json()
        return data.get('result', [])
    except requests.RequestException as e:
        return {"error": str(e)}

def get_binance_prices():
    # Function to fetch the latest price from Binance API
    try:
        response = requests.get('https://api.binance.com/api/v3/ticker/price')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def get_kraken_prices():
    # Function to fetch the latest price from Kraken API
    try:
        response = requests.get('https://api.kraken.com/0/public/Ticker')
        response.raise_for_status()
        data = response.json()
        return data.get('result', {})
    except requests.RequestException as e:
        return {"error": str(e)}

def get_yahoo_prices():
    # Function to fetch the latest price from Yahoo Finance API
    try:
        response = requests.get('https://query1.finance.yahoo.com/v7/finance/quote?symbols=BTC-USD')
        response.raise_for_status()
        data = response.json()
        return data.get('quoteResponse', {}).get('result', [])
    except requests.RequestException as e:
        return {"error": str(e)}

def get_luno_prices():
    # Placeholder for Luno API integration
    return {"price": "Real-time price from Luno"}

def get_remitano_prices():
    # Placeholder for Remitano API integration
    return {"price": "Real-time price from Remitano"}

def get_kucoin_prices():
    # Placeholder for KuCoin API integration
    return {"price": "Real-time price from KuCoin"}
