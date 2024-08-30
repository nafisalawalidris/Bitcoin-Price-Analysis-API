from pydantic import BaseModel
from datetime import date

# Define Pydantic models for request and response handling
class BitcoinPriceBase(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

    class Config:
        orm_mode = True

class BitcoinPriceCreate(BitcoinPriceBase):
    pass

class BitcoinPriceResponse(BitcoinPriceBase):
    class Config:
        orm_mode = True
