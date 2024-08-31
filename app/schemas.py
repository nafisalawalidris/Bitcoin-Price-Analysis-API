from typing import List
from pydantic import BaseModel
from datetime import date
from app.schemas import Price 

class PriceBase(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

    class Config:
        orm_mode = True

class Price(PriceBase):
    id: int

class PriceList(BaseModel):
    prices: List[Price]

    class Config:
        orm_mode = True
