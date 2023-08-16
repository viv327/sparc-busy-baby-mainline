from datetime import datetime, date

from pydantic import BaseModel, validator
from typing import List, Optional


class SleepRecord(BaseModel):
    start_time: str
    end_time: str


class BottleFeed(BaseModel):
    time: str
    volume: int


class NurseFeed(BaseModel):
    start_time: str
    end_time: str


class SolidFood(BaseModel):
    time: str
    type: str


class DiaperPee(BaseModel):
    time: str


class DiaperPoo(BaseModel):
    time: str


class Bath(BaseModel):
    time: str


class Vaccine(BaseModel):
    type: str


class Medicine(BaseModel):
    time: str
    type: Optional[str]


class DailyRecord(BaseModel):
    baby_id: str
    record_date: date
    sleep_records: Optional[List[SleepRecord]] = []
    bottle_feeds: Optional[List[BottleFeed]] = []
    nurse_feeds: Optional[List[NurseFeed]] = []
    solid_foods: Optional[List[SolidFood]] = []
    diaper_pees: Optional[List[DiaperPee]] = []
    diaper_poos: Optional[List[DiaperPoo]] = []
    baths: Optional[List[Bath]] = []
    vaccines: Optional[List[Vaccine]] = []
    medicines: Optional[List[Medicine]] = []

    @validator("record_date", pre=True)
    def parse_record_date(cls, value):
        return datetime.strptime(value, "%Y-%m-%d").date()
