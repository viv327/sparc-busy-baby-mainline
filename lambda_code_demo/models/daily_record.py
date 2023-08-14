from datetime import datetime

from pydantic import BaseModel
from typing import List


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
    type: str


class DailyRecord(BaseModel):
    sleep_records: List[SleepRecord]
    bottle_feeds: List[BottleFeed]
    nurse_feeds: List[NurseFeed]
    solid_foods: List[SolidFood]
    diaper_pees: List[DiaperPee]
    diaper_poos: List[DiaperPoo]
    baths: List[Bath]
    vaccines: List[Vaccine]
    medicines: List[Medicine]