from pydantic import BaseModel
from typing import Optional
from datetime import date

class BitcoinPrice(BaseModel):
    id: Optional[int]
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int

    class Config:
        orm_mode = True
