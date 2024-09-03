from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models

# Get all historical prices
def get_all_prices(db: Session):
    """
    Retrieve all historical Bitcoin prices from the database.

    Args:
    - db (Session): The SQLAlchemy database session.

    Returns:
    - List of BitcoinPrice objects representing all historical prices.
    """
    return db.query(models.BitcoinPrice).all()

# Get historical prices by year
def get_prices_by_year(db: Session, year: int):
    """
    Retrieve Bitcoin prices for a specific year from the database.

    Args:
    - db (Session): The SQLAlchemy database session.
    - year (int): The year for which to fetch prices.

    Returns:
    - List of BitcoinPrice objects representing prices for the specified year.
    """
    try:
        prices = db.query(models.BitcoinPrice).filter(func.extract('year', models.BitcoinPrice.date) == year).all()
        if not prices:
            raise HTTPException(status_code=404, detail="Prices not found for the given year")
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return db.query(models.BitcoinPrice).filter(func.extract('year', models.BitcoinPrice.date) == year).all()

# Get historical prices by halving event
def get_prices_by_halving(db: Session, halving_number: int):
    """
    Retrieve Bitcoin prices around specific Bitcoin halving events from the database.

    Args:
    - db (Session): The SQLAlchemy database session.
    - halving_number (int): The halving event number (e.g., 1, 2, 3, etc.).

    Returns:
    - List of BitcoinPrice objects representing prices around the specified halving event.
    """
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
    """
    Retrieve Bitcoin prices across all halving periods from the database.

    Args:
    - db (Session): The SQLAlchemy database session.

    Returns:
    - List of BitcoinPrice objects representing prices across all halving periods.
    """
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
