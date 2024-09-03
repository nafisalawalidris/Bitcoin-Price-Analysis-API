from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas

def get_all_prices(db: Session):
    return db.query(models.BitcoinPrice).all()

def get_prices_by_year(db: Session, year: int):
    return db.query(models.BitcoinPrice).filter(func.date_part('year', models.BitcoinPrice.date) == year).all()

def get_prices_by_halving(db: Session, halving_number: int):
    # Placeholder logic; adjust based on your needs
    return db.query(models.BitcoinPrice).filter(models.BitcoinPrice.date.between(start_date, end_date)).all()

def get_prices_across_halvings(db: Session):
    # Placeholder logic; you might need to define halving periods
    return db.query(models.BitcoinPrice).all()
