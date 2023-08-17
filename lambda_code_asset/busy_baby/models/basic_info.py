from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal


class Growth(BaseModel):
    record_datetime: str
    height: Optional[str]
    weight: Optional[str]
    head_circumference: Optional[str]


class Vaccine(BaseModel):
    record_datetime: str
    vaccine_type: str


class BabyProfile(BaseModel):
    baby_id: str
    first_name: str
    last_name: str
    gender: str
    birthday: str
    growth_record: Optional[List[Growth]] = []
    vaccine_record: Optional[List[Vaccine]] = []
