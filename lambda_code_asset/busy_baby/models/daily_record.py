from datetime import datetime, date

from pydantic import BaseModel, validator
from typing import List, Optional


class SleepRecord(BaseModel):
    start_time: Optional[str]
    end_time: Optional[str]
    sleep_note: str


class BottleFeed(BaseModel):
    time: str
    volume: int
    formula_note: str


class NurseFeed(BaseModel):
    start_time: Optional[str]
    end_time: Optional[str]
    nursing_note: str


class SolidFood(BaseModel):
    time: str
    food_type: str
    food_note: str


class DiaperPee(BaseModel):
    time: str
    diaper_note: str


class DiaperPoo(BaseModel):
    time: str
    diaper_note: str


class Bath(BaseModel):
    time: str
    bath_note: str


class Medicine(BaseModel):
    time: str
    med_type: Optional[str]
    med_note: str


class DailyRecord(BaseModel):
    baby_id: str
    record_date: str # https://aws.amazon.com/blogs/database/working-with-date-and-timestamp-data-types-in-amazon-dynamodb/
    sleep_records: Optional[List[SleepRecord]] = []
    bottle_feeds: Optional[List[BottleFeed]] = []
    nurse_feeds: Optional[List[NurseFeed]] = []
    solid_foods: Optional[List[SolidFood]] = []
    diaper_pees: Optional[List[DiaperPee]] = []
    diaper_poos: Optional[List[DiaperPoo]] = []
    baths: Optional[List[Bath]] = []
    medicines: Optional[List[Medicine]] = []

