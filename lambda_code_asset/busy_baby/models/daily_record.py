from datetime import datetime, date

from pydantic import BaseModel, validator
from typing import List, Optional


class SleepRecord(BaseModel):
    start_time: datetime
    end_time: datetime


class BottleFeed(BaseModel):
    time: datetime
    volume: int


class NurseFeed(BaseModel):
    start_time: datetime
    end_time: datetime


class SolidFood(BaseModel):
    time: datetime
    type: str


class DiaperPee(BaseModel):
    time: datetime


class DiaperPoo(BaseModel):
    time: datetime


class Bath(BaseModel):
    time: datetime


class Vaccine(BaseModel):
    type: str


class Medicine(BaseModel):
    time: datetime
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
