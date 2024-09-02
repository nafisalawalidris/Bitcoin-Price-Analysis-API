from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models

# Get all historical prices
def get_all_prices(db: Session):
    return db.query(models.BitcoinPrice).all()

# Get historical prices by year
def get_prices_by_year(db: Session, year: int):
    return db.query(models.BitcoinPrice).filter(func.extract('year', models.BitcoinPrice.date) == year).all()

# Get historical prices by halving event
def get_prices_by_halving(db: Session, halving_number: int):
    # Example data - adjust based on actual halving event dates
    halving_dates = {
        1: ('2012-11-28', '2013-01-01'),
        2: ('2016-07-09', '2016-08-01'),
        3: ('2020-05-11', '2020-06-01'),
        4: ('2024-04-01', '2024-05-01')  
    }
    start_date, end_date = halving_dates.get(halving_number, ('1970-01-01', '2100-01-01'))
    return db.query(models.BitcoinPrice).filter(models.BitcoinPrice.date.between(start_date, end_date)).all()

# Get historical prices across all halving periods
def get_prices_across_halvings(db: Session):
    # Example data - adjust based on actual halving event dates
    halving_dates = [
        ('2012-11-28', '2013-01-01'),
        ('2016-07-09', '2016-08-01'),
        ('2020-05-11', '2020-06-01'),
        ('2024-04-01', '2024-05-01')  
    ]
    prices = []
    for start_date, end_date in halving_dates:
        prices.extend(db.query(models.BitcoinPrice).filter(models.BitcoinPrice.date.between(start_date, end_date)).all())
    return prices
