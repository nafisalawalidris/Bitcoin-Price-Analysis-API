from datetime import datetime
from typing import List, Dict, Any
import requests

# Function to parse a date string to a datetime object
def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected format: YYYY-MM-DD")

# Function to format a datetime object to a string
def format_date(date: datetime) -> str:
    return date.strftime('%Y-%m-%d')

# Function to validate that required fields are present in the input data
def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

# Function to convert data to a dictionary with specific keys
def data_to_dict(data: Any, keys: List[str]) -> Dict[str, Any]:
    return {key: getattr(data, key, None) for key in keys}

# Function to calculate percentage change
def calculate_percentage_change(old_value: float, new_value: float) -> float:
    if old_value == 0:
        raise ValueError("Old value cannot be zero for percentage change calculation.")
    return ((new_value - old_value) / old_value) * 100

# Function to validate price data
def validate_price_data(data: Dict[str, Any]) -> None:
    required_fields = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
    validate_required_fields(data, required_fields)
    
    # Additional validation checks could be added here
    if not isinstance(data['volume'], int) or data['volume'] < 0:
        raise ValueError("Volume must be a non-negative integer")

# Example function to ensure proper date format in API responses
def ensure_date_format(data: Dict[str, Any], date_key: str) -> None:
    if date_key in data:
        try:
            data[date_key] = format_date(parse_date(data[date_key]))
        except ValueError:
            raise ValueError(f"Invalid date format in field: {date_key}")

# Example function to handle errors in a consistent manner
def handle_error(message: str) -> Dict[str, Any]:
    return {"error": message}

def fetch_bybit_price():
    try:
        response = requests.get("https://api.bybit.com/v2/public/tickers?symbol=BTCUSD")
        data = response.json()
        return data.get("result", [{}])[0].get("last_price")
    except Exception as e:
        # Log the error or handle it as needed
        return None

def fetch_binance_price():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        data = response.json()
        return data.get("price")
    except Exception as e:
        # Log the error or handle it as needed
        return None

def fetch_coinbase_price():
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/bitcoin-usd/spot")
        data = response.json()
        return data.get("data", {}).get("amount")
    except Exception as e:
        # Log the error or handle it as needed
        return None

def fetch_kucoin_price():
    try:
        response = requests.get("https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT")
        data = response.json()
        return data.get("data", {}).get("price")
    except Exception as e:
        # Log the error or handle it as needed
        return None
