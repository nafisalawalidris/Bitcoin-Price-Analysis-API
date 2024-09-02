# schemas.py
from pydantic import BaseModel
from datetime import date

class BitcoinPrice(BaseModel):
    id: int
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float
    market_cap: float

    class Config:
        orm_mode = True
