import boto3
import logging
import dateutil.parser
from datetime import timedelta, datetime
from .constants import BABY_PROFILE_DDB_TABLE, DAILY_RECORD_DDB_TABLE, DEMO_BABY_ID
from .models.basic_info import Growth, BabyProfile, Vaccine
from .models.daily_record import SleepRecord, BottleFeed, NurseFeed, SolidFood, DiaperPee, DiaperPoo, Bath, Medicine
from .models.daily_record import DailyRecord
from .utils import format_timedelta
from .persistance.ddb_item import BabyProfileDDBItem

dynamodb = boto3.resource("dynamodb")  # create dynamodb client using boto3 API
baby_profile_table = dynamodb.Table(BABY_PROFILE_DDB_TABLE)  # create dynamodb table handle
daily_record_table = dynamodb.Table(DAILY_RECORD_DDB_TABLE)  # create dynamodb table handle


logger = logging.getLogger(__name__)


def create_baby(first_name, last_name, gender, birthday, delivery_time):

    # Create BabyProfile object
    baby_id = DEMO_BABY_ID  # use dummy ID for demo purpose, should use UUID otherwise
    baby_profile = BabyProfile(
        baby_id=baby_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birthday=birthday,
        delivery_time = delivery_time
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


def add_vaccine_record(baby_id, record_date, vaccine_type, vaccine_note):
    try:
        vaccine_record = Vaccine(
            record_date=record_date,
            vaccine_type=vaccine_type,
            vaccine_note=vaccine_note
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


def add_sleep_record(baby_id, date, start_time, end_time, sleep_note):
    try:

        if start_time:
            # start_time = datetime.strptime(date + " " + start_time, "%Y-%m-%d %H:%M").isoformat()
            sleep_records = SleepRecord(
                start_time=start_time,
                end_time=end_time,
                sleep_note = sleep_note
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

        else:  # start_time is None but not end_time
            # read the DDBi tem first, find the last element from the list, then update
            # end_time = datetime.strptime(date + " " + end_time, "%Y-%m-%d %H:%M").isoformat()
            item = daily_record_table.get_item(
                Key={
                    "baby_id": baby_id,
                    "record_date": date
                }
            )['Item']

            # convert to DailyRecord object
            daily_record = DailyRecord(**item)

            last_item_index = str(len(daily_record.sleep_records) - 1)

            result = daily_record_table.update_item(
                Key={
                    "baby_id": baby_id,
                    "record_date": date
                },
                UpdateExpression="set sleep_records[" + last_item_index + "].end_time = :i",
                ExpressionAttributeValues={
                    ':i': end_time,
                },
                ReturnValues="UPDATED_NEW"
            )

        logger.info(result)

        return "Success"
    except Exception as e:
        logger.error("Failed to add sleep record")
        raise e


def add_bottle_feed(baby_id, date, time, volume, formula_note):
    try:
        bottle_feeds = BottleFeed(
            time=time,
            volume=volume,
            formula_note = formula_note
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


def add_nurse_feed(baby_id, date, start_time, end_time, nursing_note):
    try:
        if start_time:
            nurse_feeds = NurseFeed(
                start_time=start_time,
                end_time=end_time,
                nursing_note = nursing_note
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
            item = daily_record_table.get_item(
                Key={
                    "baby_id": baby_id,
                    "record_date": date
                }
            )['Item']

            # convert to DailyRecord object
            daily_record = DailyRecord(**item)

            last_item_index = str(len(daily_record.nurse_feeds) - 1)

            result = daily_record_table.update_item(
                Key={
                    "baby_id": baby_id,
                    "record_date": date
                },
                UpdateExpression="set nurse_feeds[" + last_item_index + "].end_time = :i",
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


def add_solid_food(baby_id, date, time, food_type, food_note):
    try:
        solid_foods = SolidFood(
            time=time,
            food_type=food_type,
            food_note = food_note
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


def add_diaper_pee(baby_id, date, time, diaper_note):
    try:
        diaper_pees = DiaperPee(
            time=time,
            diaper_note = diaper_note
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


def add_diaper_poo(baby_id, date, time, diaper_note):
    try:
        diaper_poos = DiaperPoo(
            time=time,
            diaper_note = diaper_note
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


def add_bath(baby_id, date, time, bath_note):
    try:
        baths = Bath(
            time=time,
            bath_note = bath_note
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


def add_medicine(baby_id, date, time, med_type, med_note):
    try:
        medicines = Medicine(
            time=time,
            med_type=med_type,
            med_note = med_note
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


def get_most_recent_height(baby_id):
    item = baby_profile_table.get_item(
        Key={
            "baby_id": baby_id,
        }
    )['Item']

    baby_profile = BabyProfile(**item)
    growth_len = len(baby_profile.growth_record)
    last_height = None
    last_date = None
    for i in range(growth_len-1, -1, -1):
        if baby_profile.growth_record[i].height:
            last_height = baby_profile.growth_record[i].height
            last_date = baby_profile.growth_record[i].record_date
            break

    return last_height, last_date


def get_most_recent_weight(baby_id):
    item = baby_profile_table.get_item(
        Key={
            "baby_id": baby_id,
        }
    )['Item']

    baby_profile = BabyProfile(**item)
    growth_len = len(baby_profile.growth_record)
    last_weight = None
    last_date = None
    for i in range(growth_len-1, -1, -1):
        if baby_profile.growth_record[i].weight:
            last_weight = baby_profile.growth_record[i].weight
            last_date = baby_profile.growth_record[i].record_date
            break

    return last_weight, last_date


def get_most_recent_head_circumference(baby_id):
    item = baby_profile_table.get_item(
        Key={
            "baby_id": baby_id,
        }
    )['Item']

    baby_profile = BabyProfile(**item)
    growth_len = len(baby_profile.growth_record)
    last_head_circumference = None
    last_date = None
    for i in range(growth_len-1, -1, -1):
        if baby_profile.growth_record[i].head_circumference:
            last_head_circumference = baby_profile.growth_record[i].head_circumference
            last_date = baby_profile.growth_record[i].record_date
            break

    return last_head_circumference, last_date


def get_most_recent_vaccine(baby_id):
    item = baby_profile_table.get_item(
        Key={
            "baby_id": baby_id,
        }
    )['Item']

    baby_profile = BabyProfile(**item)
    vaccine_len = len(baby_profile.vaccine_record)
    last_vaccine = None
    last_date = None
    if vaccine_len > 0:
        last_vaccine = baby_profile.vaccine_record[-1].vaccine_type
        last_date = baby_profile.vaccine_record[-1].record_date

    return last_vaccine, last_date


def get_most_recent_sleep_start(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    sleep_len = len(daily_record.sleep_records)
    last_sleep_start = None

    for i in range(sleep_len-1, -1, -1):
        if daily_record.sleep_records[i].start_time:
            last_sleep_start = daily_record.sleep_records[i].start_time
            break
    parsed_datetime = datetime.strptime(last_sleep_start, "%Y-%m-%dT%H:%M:%S")
    formatted_time = parsed_datetime.strftime("%I:%M%p")

    return formatted_time


def get_most_recent_sleep_end(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    sleep_len = len(daily_record.sleep_records)
    last_sleep_end = None

    for i in range(sleep_len-1, -1, -1):
        if daily_record.sleep_records[i].end_time:
            last_sleep_end = daily_record.sleep_records[i].end_time
            break
    parsed_datetime = datetime.strptime(last_sleep_end, "%Y-%m-%dT%H:%M:%S")
    formatted_time = parsed_datetime.strftime("%I:%M%p")
    return formatted_time


def get_most_recent_sleep_duration(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    sleep_len = len(daily_record.sleep_records)
    result = None

    for i in range(sleep_len-1, -1, -1):
        if daily_record.sleep_records[i].start_time and daily_record.sleep_records[i].end_time:
            last_sleep_start = daily_record.sleep_records[i].start_time
            last_sleep_end = daily_record.sleep_records[i].end_time
            duration = dateutil.parser.parse(last_sleep_end) - dateutil.parser.parse(last_sleep_start)
            result = format_timedelta(duration)
            break
    return result

def get_total_sleep_time(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    sleep_len = len(daily_record.sleep_records)
    total_sleep_time = timedelta()

    for i in range(sleep_len-1, -1, -1):
        if daily_record.sleep_records[i].start_time and daily_record.sleep_records[i].end_time:
            last_sleep_start = daily_record.sleep_records[i].start_time
            last_sleep_end = daily_record.sleep_records[i].end_time
            total_sleep_time += dateutil.parser.parse(last_sleep_end) - dateutil.parser.parse(last_sleep_start)
    result = format_timedelta(total_sleep_time)

    return result


def get_total_sleep_count(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    sleep_len = len(daily_record.sleep_records)
    total_sleep_count = 0

    for i in range(sleep_len-1, -1, -1):
        if daily_record.sleep_records[i].start_time and daily_record.sleep_records[i].end_time:
            total_sleep_count += 1

    return str(total_sleep_count)


def get_most_recent_bottle_feed(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    bottle_feed_len = len(daily_record.bottle_feeds)
    last_bottle_volume = None
    last_bottle_time = None

    if bottle_feed_len > 0:
        last_bottle_volume = daily_record.bottle_feeds[-1].volume
        last_bottle_time = daily_record.bottle_feeds[-1].time

    parsed_datetime = datetime.strptime(last_bottle_time, "%Y-%m-%dT%H:%M:%S")
    formatted_time = parsed_datetime.strftime("%I:%M%p")
    return str(last_bottle_volume), formatted_time


def get_total_bottle_feed_volume(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    bottle_feed_len = len(daily_record.bottle_feeds)
    total_bottle_volume = 0

    for i in range(bottle_feed_len-1, -1, -1):
        if daily_record.bottle_feeds[i].volume:
            total_bottle_volume += daily_record.bottle_feeds[i].volume
    return str(total_bottle_volume)


def get_total_bottle_feed_count(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    total_bottle_count = len(daily_record.bottle_feeds)

    return str(total_bottle_count)


def get_most_recent_nurse_feed_end(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    nurse_len = len(daily_record.nurse_feeds)
    last_nurse_feed_end = None

    for i in range(nurse_len-1, -1, -1):
        if daily_record.nurse_feeds[i].end_time:
            last_nurse_feed_end = daily_record.nurse_feeds[i].end_time
            break
    parsed_datetime = datetime.strptime(last_nurse_feed_end, "%Y-%m-%dT%H:%M:%S")
    formatted_time = parsed_datetime.strftime("%I:%M%p")
    return formatted_time


def get_total_nurse_feed_count(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    nurse_len = len(daily_record.nurse_feeds)
    total_nurse_count = 0

    for i in range(nurse_len-1, -1, -1):
        if daily_record.nurse_feeds[i].start_time and daily_record.nurse_feeds[i].end_time:
            total_nurse_count += 1

    return str(total_nurse_count)


def get_most_recent_solid_food(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    solid_len = len(daily_record.solid_foods)
    last_solid_food_type = None
    last_solid_food_time = None

    if solid_len > 0:
        last_solid_food_type = daily_record.solid_foods[-1].food_type
        last_solid_food_time = daily_record.solid_foods[-1].time
    parsed_datetime = datetime.strptime(last_solid_food_time, "%Y-%m-%dT%H:%M:%S")
    formatted_time = parsed_datetime.strftime("%I:%M%p")
    return last_solid_food_type, formatted_time


def get_total_solid_food_count(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    total_solid_count = len(daily_record.solid_foods)

    return str(total_solid_count)


def get_all_solid_food_types(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    solid_len = len(daily_record.solid_foods)
    solid_list = []
    for i in range(solid_len - 1, -1, -1):
        solid_list.append(daily_record.solid_foods[i].food_type)

    return set(solid_list)


def get_most_recent_diaper_pee(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    last_pee = daily_record.diaper_pees[-1].time
    parsed_datetime = datetime.strptime(last_pee, "%Y-%m-%dT%H:%M:%S")
    formatted_time = parsed_datetime.strftime("%I:%M%p")
    return formatted_time


def get_total_diaper_pee_count(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    total_pee_count = len(daily_record.diaper_pees)

    return str(total_pee_count)


def get_most_recent_diaper_poo(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    last_poo = daily_record.diaper_poos[-1].time
    parsed_datetime = datetime.strptime(last_poo, "%Y-%m-%dT%H:%M:%S")
    formatted_time = parsed_datetime.strftime("%I:%M%p")
    return formatted_time


def get_total_diaper_poo_count(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    total_poo_count = len(daily_record.diaper_poos)

    return str(total_poo_count)


def get_most_recent_bath(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    last_bath = daily_record.baths[-1].time
    parsed_datetime = datetime.strptime(last_bath, "%Y-%m-%dT%H:%M:%S")
    formatted_time = parsed_datetime.strftime("%I:%M%p")
    return formatted_time


def get_most_recent_medicine(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    last_medicine_type = daily_record.medicines[-1].med_type
    last_medicine_time = daily_record.medicines[-1].time
    parsed_datetime = datetime.strptime(last_medicine_time, "%Y-%m-%dT%H:%M:%S")
    formatted_time = parsed_datetime.strftime("%I:%M%p")
    return last_medicine_type, formatted_time


def get_total_medicine_count(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    total_med_count = len(daily_record.medicines)

    return str(total_med_count)


def delete_most_recent_sleep_record(baby_id, record_date):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    # convert to DailyRecord object
    daily_record = DailyRecord(**item)
    sleep_index = str(len(daily_record.sleep_records) - 1)

    result = daily_record_table.update_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        },
        UpdateExpression="REMOVE sleep_records[" + sleep_index + "]",
        # ExpressionAttributeValues={
        #     ':i': end_time
        # },
        ReturnValues="UPDATED_NEW"
    )

    return "Success"


def update_most_recent_vaccine_date(baby_id, vaccine_date):
    item = baby_profile_table.get_item(
        Key={
            "baby_id": baby_id,
        }
    )['Item']
    baby_profile = BabyProfile(**item)
    last_item_index = str(len(baby_profile.vaccine_record) - 1)

    result = baby_profile_table.update_item(
        Key={
            "baby_id": baby_id,
        },
        UpdateExpression="set vaccine_record[" + last_item_index + "].record_date = :i",
        ExpressionAttributeValues={
            ':i': vaccine_date
        },
        ReturnValues="UPDATED_NEW"
    )

    logger.info(result)

    return "Success"


def update_most_recent_sleep_record(baby_id, record_date, start_time, end_time):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    last_item_index = str(len(daily_record.sleep_records) - 1)

    if start_time:
        result = daily_record_table.update_item(
            Key={
                "baby_id": baby_id,
                "record_date": record_date
            },
            UpdateExpression="set sleep_records[" + last_item_index + "].start_time = :i",
            ExpressionAttributeValues={
                ':i': start_time
            },
            ReturnValues="UPDATED_NEW"
        )
    else:
        result = daily_record_table.update_item(
            Key={
                "baby_id": baby_id,
                "record_date": record_date
            },
            UpdateExpression="set sleep_records[" + last_item_index + "].end_time = :i",
            ExpressionAttributeValues={
                ':i': end_time
            },
            ReturnValues="UPDATED_NEW"
        )

    logger.info(result)
    return "Success"


def update_most_recent_bottle_feed(baby_id, record_date, formula_volume):
    item = daily_record_table.get_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        }
    )['Item']

    daily_record = DailyRecord(**item)
    last_item_index = str(len(daily_record.bottle_feeds) - 1)

    result = daily_record_table.update_item(
        Key={
            "baby_id": baby_id,
            "record_date": record_date
        },
        UpdateExpression="set bottle_feeds[" + last_item_index + "].volume = :i",
        ExpressionAttributeValues={
            ':i': formula_volume
        },
        ReturnValues="UPDATED_NEW"
    )

    logger.info(result)
    return "Success"

