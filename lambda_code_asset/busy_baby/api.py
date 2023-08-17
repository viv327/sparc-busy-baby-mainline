import boto3
import logging
import os
import uuid
from .constants import BABY_PROFILE_DDB_TABLE, DAILY_RECORD_DDB_TABLE, DEMO_BABY_ID
from .models.basic_info import Growth, BabyProfile, Vaccine
from .models.daily_record import DailyRecord
from .persistance.ddb_item import BabyProfileDDBItemAttrs, BabyProfileDDBItem, DailyRecordDDBItemAttrs, DailyRecordDDBItem

dynamodb = boto3.resource("dynamodb")  # create dynamodb client using boto3 API
baby_profile_table = dynamodb.Table(BABY_PROFILE_DDB_TABLE)  # create dynamodb table handle
daily_record_table = dynamodb.Table(DAILY_RECORD_DDB_TABLE)  # create dynamodb table handle


logger = logging.getLogger(__name__)


def create_baby(first_name, last_name, gender, birthday):

    # Create BabyProfile object
    baby_id = DEMO_BABY_ID  # use dummy ID for demo purpose, should use UUID otherwise
    baby_profile = BabyProfile(
        baby_id=baby_id,
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
    return baby_id


def add_growth_record(baby_id, record_datetime, height, weight, head_circumference):
    try:
        growth_record = Growth(
            record_datetime=record_datetime,
            height=height,
            weight=weight,
            head_circumference=head_circumference
        )

        result = baby_profile_table.update_item(
            Key={
                "baby_id": baby_id
            },
            UpdateExpression="set growth_record = list_append(growth_record, :i)",
            ExpressionAttributeValues={
                ':i': [growth_record.dict()]
            },
            ReturnValues="UPDATED_NEW"
        )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to update baby profile")
        raise e


def add_vaccine_record(baby_id, record_datetime, vaccine_type):
    try:
        vaccine_record = Vaccine(
            record_datetime=record_datetime,
            vaccine_type=vaccine_type,
        )

        result = baby_profile_table.update_item(
            Key={
                "baby_id": baby_id
            },
            UpdateExpression="set vaccine_record = list_append(vaccine_record, :i)",
            ExpressionAttributeValues={
                ':i': [vaccine_record.dict()]
            },
            ReturnValues="UPDATED_NEW"
        )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to update baby profile")
        raise e
