from enum import Enum

from pydantic import BaseModel, Field

from ..models.basic_info import BabyProfile
from ..models.daily_record import DailyRecord

class BabyProfileDDBItemAttrs(Enum):
    BABY_ID = "baby_id" # partition key
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    GENDER = "gender"
    BIRTHDAY = "birthday"
    GROWTH_RECORD = "growth_record"

    def __init__(self, ddb_attr):
        self.ddb_attr = ddb_attr


class DailyRecordDDBItemAttrs(Enum):
    BABY_ID = "baby_id" # partition key
    RECORD_DATE = "record_date" # sort key
    SLEEP_RECORDS = "sleep_records"
    BOTTLE_FEEDS = "bottle_feeds"
    NURSE_FEEDS = "nurse_feeds"
    SOLID_FOODS = "solid_foods"
    DIAPER_PEES = "diaper_pees"
    DIAPER_POOS = "diaper_poos"
    BATHS = "baths"
    VACCINES = "vaccines"
    MEDICINES = "medicines"

    def __init__(self, ddb_attr):
        self.ddb_attr = ddb_attr


class BabyProfileDDBItem(BaseModel):
    baby_id: str = Field(alias=BabyProfileDDBItemAttrs.BABY_ID.ddb_attr)
    first_name: str = Field(alias=BabyProfileDDBItemAttrs.FIRST_NAME.ddb_attr)
    last_name: str = Field(alias=BabyProfileDDBItemAttrs.LAST_NAME.ddb_attr)
    gender: str = Field(alias=BabyProfileDDBItemAttrs.GENDER.ddb_attr)
    birthday: str = Field(alias=BabyProfileDDBItemAttrs.BIRTHDAY.ddb_attr)
    growth_record: list = Field(alias=BabyProfileDDBItemAttrs.GROWTH_RECORD.ddb_attr)

    def to_entity(self):
        return BabyProfile(
            baby_id=self.baby_id,
            first_name=self.first_name,
            last_name=self.last_name,
            gender=self.gender,
            birthday=self.birthday,
            growth_record=self.growth_record
        )

    @staticmethod
    def from_entity(baby_profile: BabyProfile):
        return BabyProfileDDBItem(
            baby_id=baby_profile.baby_id,
            first_name=baby_profile.first_name,
            last_name=baby_profile.last_name,
            gender=baby_profile.gender,
            birthday=baby_profile.birthday,
            growth_record=baby_profile.growth_record
        )

    def to_ddb(self):
        return self.dict(by_alias=True)


class DailyRecordDDBItem(BaseModel):
    baby_id: str = Field(alias=DailyRecordDDBItemAttrs.BABY_ID.ddb_attr)
    sleep_records: list = Field(alias=DailyRecordDDBItemAttrs.SLEEP_RECORDS.ddb_attr)
    bottle_feeds: list = Field(alias=DailyRecordDDBItemAttrs.BOTTLE_FEEDS.ddb_attr)
    nurse_feeds: list = Field(alias=DailyRecordDDBItemAttrs.NURSE_FEEDS.ddb_attr)
    solid_foods: list = Field(alias=DailyRecordDDBItemAttrs.SOLID_FOODS.ddb_attr)
    diaper_pees: list = Field(alias=DailyRecordDDBItemAttrs.DIAPER_PEES.ddb_attr)
    diaper_poos: list = Field(alias=DailyRecordDDBItemAttrs.DIAPER_POOS.ddb_attr)
    baths: list = Field(alias=DailyRecordDDBItemAttrs.BATHS.ddb_attr)
    vaccines: list = Field(alias=DailyRecordDDBItemAttrs.VACCINES.ddb_attr)
    medicines: list = Field(alias=DailyRecordDDBItemAttrs.MEDICINES.ddb_attr)

    def to_entity(self):
        return DailyRecord(
            baby_id=self.baby_id,
            sleep_records=self.sleep_records,
            bottle_feeds=self.bottle_feeds,
            nurse_feeds=self.nurse_feeds,
            solid_foods=self.solid_foods,
            diaper_pees=self.diaper_pees,
            diaper_poos=self.diaper_poos,
            baths=self.baths,
            vaccines=self.vaccines,
            medicines=self.medicines
        )

    @staticmethod
    def from_entity(daily_record: DailyRecord):
        return DailyRecord(
            baby_id=daily_record.baby_id,
            sleep_records=daily_record.sleep_records,
            bottle_feeds=daily_record.bottle_feeds,
            nurse_feeds=daily_record.nurse_feeds,
            solid_foods=daily_record.solid_foods,
            diaper_pees=daily_record.diaper_pees,
            diaper_poos=daily_record.diaper_poos,
            baths=daily_record.baths,
            vaccines=daily_record.vaccines,
            medicines=daily_record.medicines
        )

    def to_ddb(self):
        return self.dict(by_alias=True)
