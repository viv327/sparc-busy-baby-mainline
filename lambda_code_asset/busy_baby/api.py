import boto3
import logging
import os
import uuid
from .constants import BABY_PROFILE_DDB_TABLE, DAILY_RECORD_DDB_TABLE, DEMO_BABY_ID
from .models.basic_info import Growth, BabyProfile, Vaccine
from .models.daily_record import SleepRecord, BottleFeed, NurseFeed, SolidFood, DiaperPee, DiaperPoo, Bath, Medicine
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


def add_growth_record(baby_id, record_date, height, weight, head_circumference):
    try:
        growth_record = Growth(
            record_date=record_date,
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


def add_vaccine_record(baby_id, record_date, vaccine_type):
    try:
        vaccine_record = Vaccine(
            record_date=record_date,
            vaccine_type=vaccine_type,
        )

        result = baby_profile_table.update_item(
            Key={
                "baby_id": baby_id
            },
            UpdateExpression="set vaccine_record = list_append(if_not_exists(vaccine_record, :empty_list), :i)",
            ExpressionAttributeValues={
                ':i': [vaccine_record.dict()],
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to update baby profile")
        raise e


def add_sleep_record(baby_id, date, start_time, end_time):
    try:
        if start_time:
            sleep_records = SleepRecord(
                start_time=start_time,
                end_time=end_time
            )
            result = daily_record_table.update_item(
                Key={
                    "baby_id": baby_id,
                    "record_date": date
                },
                UpdateExpression="set sleep_records = list_append(if_not_exists(sleep_records, :empty_list), :i)",
                ExpressionAttributeValues={
                    ':i': [sleep_records.dict()],
                    ':empty_list': []
                },
                ReturnValues="UPDATED_NEW"
            )

        else: # start_time is None but not end_time
            # read the DDBi tem first, find the last element from the list, then update
            sleep_records = daily_record_table.get_item(
                Key={
                    "baby_id": baby_id,
                    "record_date": date
                }
            )['Item']

            last_item_index = str(len(sleep_records)-1)

            result = daily_record_table.update_item(
                Key={
                    "baby_id": baby_id,
                    "record_date": date
                },
                UpdateExpression="set sleep_records[" + last_item_index + "].end_time = :i)",
                ExpressionAttributeValues={
                    ':i': end_time
                },
                ReturnValues="UPDATED_NEW"
            )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to add sleep record")
        raise e


def add_bottle_feed(baby_id, date, time, volume):
    try:
        bottle_feeds = BottleFeed(
            time=time,
            volume=volume,
        )

        result = daily_record_table.update_item(
            Key={
                "baby_id": baby_id,
                "record_date": date
            },
            UpdateExpression="set bottle_feeds = list_append(if_not_exists(bottle_feeds, :empty_list), :i)",
            ExpressionAttributeValues={
                ':i': [bottle_feeds.dict()],
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to add bottle feed")
        raise e


def add_nurse_feed(baby_id, date, start_time, end_time):
    try:
        if start_time:
            nurse_feeds = NurseFeed(
                start_time=start_time,
                end_time=end_time
            )
            result = daily_record_table.update_item(
                Key={
                    "baby_id": baby_id,
                    "record_date": date
                },
                UpdateExpression="set nurse_feeds = list_append(if_not_exists(nurse_feeds, :empty_list), :i)",
                ExpressionAttributeValues={
                    ':i': [nurse_feeds.dict()],
                    ':empty_list': []
                },
                ReturnValues="UPDATED_NEW"
            )
        else:  # start_time is None but not end_time
            # read the DDB item first, find the last element from the list, then update
            nurse_feeds = daily_record_table.get_item(
                Key={
                    "baby_id": baby_id,
                    "record_date": date
                }
            )['Item']

            last_item_index = str(len(nurse_feeds) - 1)

            result = daily_record_table.update_item(
                Key={
                    "baby_id": baby_id,
                    "record_date": date
                },
                UpdateExpression="set nurse_feeds[" + last_item_index + "].end_time = :i)",
                ExpressionAttributeValues={
                    ':i': end_time
                },
                ReturnValues="UPDATED_NEW"
            )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to add nurse feed")
        raise e


def add_solid_food(baby_id, date, time, food_type):
    try:
        solid_foods = SolidFood(
            time=time,
            food_type=food_type,
        )

        result = daily_record_table.update_item(
            Key={
                "baby_id": baby_id,
                "record_date": date
            },
            UpdateExpression="set solid_foods = list_append(if_not_exists(solid_foods, :empty_list), :i)",
            ExpressionAttributeValues={
                ':i': [solid_foods.dict()],
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to add solid food")
        raise e


def add_diaper_pee(baby_id, date, time):
    try:
        diaper_pees = DiaperPee(
            time=time,
        )

        result = daily_record_table.update_item(
            Key={
                "baby_id": baby_id,
                "record_date": date
            },
            UpdateExpression="set diaper_pees = list_append(if_not_exists(diaper_pees, :empty_list), :i)",
            ExpressionAttributeValues={
                ':i': [diaper_pees.dict()],
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to add diaper pee")
        raise e


def add_diaper_poo(baby_id, date, time):
    try:
        diaper_poos = DiaperPoo(
            time=time,
        )

        result = daily_record_table.update_item(
            Key={
                "baby_id": baby_id,
                "record_date": date
            },
            UpdateExpression="set diaper_poos = list_append(if_not_exists(diaper_poos, :empty_list), :i)",
            ExpressionAttributeValues={
                ':i': [diaper_poos.dict()],
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to add diaper poo")
        raise e


def add_bath(baby_id, date, time):
    try:
        baths = Bath(
            time=time,
        )

        result = daily_record_table.update_item(
            Key={
                "baby_id": baby_id,
                "record_date": date
            },
            UpdateExpression="set baths = list_append(if_not_exists(baths, :empty_list), :i)",
            ExpressionAttributeValues={
                ':i': [baths.dict()],
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to add bath")
        raise e


def add_medicine(baby_id, date, time, med_type):
    try:
        medicines = Medicine(
            time=time,
            med_type=med_type
        )

        result = daily_record_table.update_item(
            Key={
                "baby_id": baby_id,
                "record_date": date
            },
            UpdateExpression="set medicines = list_append(if_not_exists(medicines, :empty_list), :i)",
            ExpressionAttributeValues={
                ':i': [medicines.dict()],
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to add medicine")
        raise e