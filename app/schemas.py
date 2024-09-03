from pydantic import BaseModel
from datetime import datetime

class BitcoinPriceBase(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

class BitcoinPriceCreate(BitcoinPriceBase):
    pass

class BitcoinPrice(BitcoinPriceBase):
    id: int

    class Config:
        orm_mode = True
