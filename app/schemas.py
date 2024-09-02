from pydantic import BaseModel
from datetime import date

class BitcoinPriceBase(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float
    market_cap: float

class BitcoinPriceCreate(BitcoinPriceBase):
    pass

class BitcoinPriceRead(BitcoinPriceBase):
    id: int

    class Config:
        orm_mode = True
