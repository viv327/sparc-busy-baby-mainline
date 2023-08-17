import json
from datetime import datetime
from busy_baby.api import create_baby, add_growth_record, add_vaccine_record
from busy_baby.constants import DEMO_BABY_ID


def dispatch(intent: str, slots: any):
    response = {}
    message = ''

    # dispatch to different service based on different intent
    if intent == "createBaby":
        first_name = slots["FirstName"]["value"]["interpretedValue"]
        last_name = slots["LastName"]["value"]["interpretedValue"]
        gender = slots["Gender"]["value"]["interpretedValue"]
        birthday = slots["Birthday"]["value"]["interpretedValue"]

        result = create_baby(first_name, last_name, gender, birthday)
        message = "Baby profile creation result: {}".format(result)

    if intent == "addGrowthRecord":
        record_datetime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')  # convert current UTC datetime to string

        if "Height" in slots and "value" in slots["Height"]:
            height = slots["Height"]["value"]["interpretedValue"]
        else:
            height = None

        if "Weight" in slots and "value" in slots["Weight"]:
            weight = slots["Weight"]["value"]["interpretedValue"]
        else:
            weight = None

        if "HeadCircumference" in slots and "value" in slots["HeadCircumference"]:
            head_circumference = slots["HeadCircumference"]["value"]["interpretedValue"]
        else:
            head_circumference = None

        result = add_growth_record(DEMO_BABY_ID, record_datetime, height, weight, head_circumference)
        message = "Update baby growth record result: {}".format(result)

    if intent == "addVaccineRecord":
        record_datetime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')  # convert current UTC datetime to string

        if "VaccineType" in slots and "value" in slots["VaccineType"]:
            vaccine_type = slots["VaccineType"]["value"]["interpretedValue"]
        else:
            vaccine_type = None

        result = add_vaccine_record(DEMO_BABY_ID, record_datetime, vaccine_type)
        message = "Update baby growth record result: {}".format(result)

    # Generate response
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent,
                "slots": slots,
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }

    '''
    - createBaby(first_name, last_name, gender, birthday)x
    - addGrowthRecord(baby_id, record_datetime, height, weight, head_circumference)
    - addVaccineRecord(baby_id, record_datetime, vaccine_type)
    - addSleepRecord(baby_id, date, start_time, end_time)
    - addBottleFeed(baby_id, date, bottle_time, volume)
    - addNurseFeed(baby_id, date, start_time, end_time)
    - addSolidFood(baby_id, date, food_time, food_type)
    - addDiaperPee(baby_id, date, pee_time)
    - addDiaperPoo(baby_id, date, poo_time)
    - addBath(baby_id, date, bath_time)
    - addVaccine(baby_id, date, vaccine_type)
    - addMedicine(baby_id, date, medicine_time, medicine_type)
    
    - getMostRecentHeight(baby_id)
    - getMostRecentWeight(baby_id)
    - getMostRecentHeadCircumference(baby_id)
    - getMostRecentVaccineDay(baby_id, date)
    - getAllVaccineTypes(baby_id, date)
    - getMostRecentSleepStart(baby_id, date)
    - getMostRecentSleepEnd(baby_id, date)
    - getMostRecentSleepDuration(baby_id, date)
    - getTotalSleepTime(baby_id, date)
    - getTotalSleepCount(baby_id, date)
    - getMostRecentBottleFeedTime(baby_id, date)
    - getMostRecentBottleFeedVolume(baby_id, date)
    - getTotalBottleFeedVolume(baby_id, date)
    - getTotalBottleFeedCount(baby_id, date)
    - getMostRecentNurseFeedEnd(baby_id, date)
    - getTotalNurseFeedCount(baby_id, date)
    - getMostRecentSolidFoodTime(baby_id, date)
    - getMostRecentSolidFoodType(baby_id, date)
    - getTotalSolidFoodCount(baby_id, date)
    - getAllSolidFoodTypes(baby_id, date)
    - getMostRecentDiaperPeeTime(baby_id, date)
    - getTotalDiaperPeeCount(baby_id, date)
    - getMostRecentDiaperPooTime(baby_id, date)
    - getTotalDiaperPooCount(baby_id, date)
    - getMostRecentBathTime(baby_id, date)
    - getMostRecentMedicineTime(baby_id, date)
    - getTotalMedicineCount(baby_id, date)
    
    - deleteMostRecentSleepRecord(baby_id)
    - updateMostRecentSleepStartRecord(baby_id, start_time)**********
    - updateMostRecentSleepEndRecord(baby_id, end_time)**********
    - updateMostRecentBottleFeed(baby_id, volume, bottle_time)
    
    
    '''
    # TODO: add more intents here, each with a handling function
    return response


def delegate(intent: str, slots: any):
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Delegate"  # let the bot decide what to do next
            },
            "intent": {
                "name": intent,
                "slots": slots
            }
        }
    }


def main(event, context):
    print('request: {}'.format(json.dumps(event)))

    intent = event["sessionState"]["intent"]["name"]
    slots = event["sessionState"]["intent"]["slots"]

    print(event["invocationSource"])
    print(intent)
    print(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        response = delegate(intent, slots)

    if event["invocationSource"] == "FulfillmentCodeHook":
        response = dispatch(intent, slots)

    return response
