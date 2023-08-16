import boto3
import logging
import os
import uuid
from .constants import BABY_PROFILE_DDB_TABLE, DAILY_RECORD_DDB_TABLE, DEMO_BABY_ID
from .models.basic_info import Growth, BabyProfile
from .models.daily_record import DailyRecord
from .persistance.ddb_item import BabyProfileDDBItemAttrs, BabyProfileDDBItem, DailyRecordDDBItemAttrs, DailyRecordDDBItem

dynamodb = boto3.resource("dynamodb")
baby_profile_table = dynamodb.Table(BABY_PROFILE_DDB_TABLE)
daily_record_table = dynamodb.Table(DAILY_RECORD_DDB_TABLE)


logger = logging.getLogger(__name__)


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


def add_growth_record(baby_id, record_datetime, height, weight, head_circumference):
    try:
        growth_record = Growth(
            record_datetime=record_datetime,
            height=height,
            weight=weight,
            head_circumference=head_circumference
        )
        update_expression = f"set {BabyProfileDDBItemAttrs.GROWTH_RECORD.ddb_attr}"
        expression_attr_values = {
            ':baby_id': baby_id,
            ':growth_record': [growth_record.dict()]
        }

        baby_profile_table.update_item(
            Key={
                BabyProfileDDBItemAttrs.BABY_ID.ddb_attr: baby_id
            },
            UpdateExpression=update_expression,
            ConditionExpression="baby_id = :baby_id",
            ExpressionAttributeValues=expression_attr_values
        )

        return "Success"
    except Exception as e:
        logger.error("Failed to update baby profile")
        raise e