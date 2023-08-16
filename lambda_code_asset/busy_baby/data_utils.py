import boto3
import os
import uuid
from .constants import BABY_PROFILE_DDB_TABLE, DAILY_RECORD_DDB_TABLE, DEMO_BABY_ID
from .models.basic_info import BabyProfile
from .models.daily_record import DailyRecord
from .persistance.ddb_item import BabyProfileDDBItem, DailyRecordDDBItem

dynamodb = boto3.resource("dynamodb")
baby_profile_table = dynamodb.Table(BABY_PROFILE_DDB_TABLE)
daily_record_table = dynamodb.Table(DAILY_RECORD_DDB_TABLE)


def create_baby(first_name, last_name, gender, birthday):

    # Create BabyProfile object
    baby_profile = BabyProfile(
        baby_id=DEMO_BABY_ID,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birthday=birthday
    )

    # Convert to DDB item
    baby_profile_ddb_item = BabyProfileDDBItem.from_entity(baby_profile)

    # Add item to database
    baby_profile_table.put_item(Item=baby_profile_ddb_item.to_ddb())

    print("Dummy: success!")

    # return "(calculated result based on DDB query, e.g,  milk intake volume)"
    return "Success"