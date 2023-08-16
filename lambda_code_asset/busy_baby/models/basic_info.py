from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class Growth(BaseModel):
    record_datetime: datetime
    height: Optional[float]
    weight: Optional[float]
    head_circumference: Optional[float]


class BabyProfile(BaseModel):
    baby_id: str
    first_name: str
    last_name: str
    gender: str
    birthday: str
    growth_record: List[Growth] = []