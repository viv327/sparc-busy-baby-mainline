import json
from datetime import datetime

from busy_baby.api import create_baby, add_growth_record, add_vaccine_record, add_bottle_feed, add_sleep_record, \
    add_nurse_feed, add_solid_food, add_diaper_pee, add_diaper_poo, add_bath, add_medicine
from busy_baby.constants import DEMO_BABY_ID, CREATE_BABY_INTENT, FIRST_NAME, LAST_NAME, GENDER, BIRTHDAY


def dispatch(intent: str, slots: any):
    response = {}
    message = ''

    # dispatch to different service based on different intent
    # if intent == "createBaby":
    #     first_name = slots["FirstName"]["value"]["interpretedValue"]
    #     last_name = slots["LastName"]["value"]["interpretedValue"]
    #     gender = slots["Gender"]["value"]["interpretedValue"]
    #     birthday = slots["Birthday"]["value"]["interpretedValue"]

    if intent == CREATE_BABY_INTENT:
        first_name = slots[FIRST_NAME]["value"]["interpretedValue"]
        last_name = slots[LAST_NAME]["value"]["interpretedValue"]
        gender = slots[GENDER]["value"]["interpretedValue"]
        birthday = slots[BIRTHDAY]["value"]["interpretedValue"]

        result = create_baby(first_name, last_name, gender, birthday)
        message = "Baby profile creation result: {}".format(result)

    if intent == "addGrowthRecord":
        record_date = slots["RecordDate"]["value"]["interpretedValue"]
        if record_date == "today":
            record_date = datetime.utcnow().strftime('%Y-%m-%d')  # convert current UTC date to strings

        if "Height" in slots and "value" in slots["Height"]:
            height = slots["Height"]["value"]["interpretedValue"]
        else:
            height = None  # because height is optional field, hence can be None if not provided by upstream (e.g, Lex)

        if "Weight" in slots and "value" in slots["Weight"]:
            weight = slots["Weight"]["value"]["interpretedValue"]
        else:
            weight = None

        if "HeadCircumference" in slots and "value" in slots["HeadCircumference"]:
            head_circumference = slots["HeadCircumference"]["value"]["interpretedValue"]
        else:
            head_circumference = None

        result = add_growth_record(DEMO_BABY_ID, record_date, height, weight, head_circumference)
        message = "Update baby growth record result: {}".format(result)

    if intent == "addVaccineRecord":
        record_date = slots["RecordDate"]["value"]["interpretedValue"]
        if record_date == "today":
            record_date = datetime.utcnow().strftime('%Y-%m-%d')  # convert current UTC date to strings

        vaccine_type = slots["VaccineType"]["value"]["interpretedValue"]
        result = add_vaccine_record(DEMO_BABY_ID, record_date, vaccine_type)
        message = "Update baby vaccine record result: {}".format(result)

    if intent == "addSleepRecord":
        record_date = datetime.utcnow().strftime('%Y-%m-%d')
        if "StartTime" in slots and "value" in slots["StartTime"]:
            start_time = slots["StartTime"]["value"]["interpretedValue"]
        else:
            start_time = None

        if "EndTime" in slots and "value" in slots["EndTime"]:
            end_time = slots["EndTime"]["value"]["interpretedValue"]
        else:
            end_time = None

        result = add_sleep_record(DEMO_BABY_ID, record_date, start_time, end_time)
        message = "Add sleep record result: {}".format(result)

    if intent == "addBottleFeed":
        record_date = datetime.utcnow().strftime('%Y-%m-%d')
        time = slots["Time"]["value"]["interpretedValue"]
        if time == "now":
            time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        volume = slots["Volume"]["value"]["interpretedValue"]
        result = add_bottle_feed(DEMO_BABY_ID, record_date, time, volume)
        message = "Add bottle feed result: {}".format(result)

    if intent == "addNurseFeed":
        record_date = datetime.utcnow().strftime('%Y-%m-%d')
        if "StartTime" in slots and "value" in slots["StartTime"]:
            start_time = slots["StartTime"]["value"]["interpretedValue"]
        else:
            start_time = None

        if "EndTime" in slots and "value" in slots["EndTime"]:
            end_time = slots["EndTime"]["value"]["interpretedValue"]
        else:
            end_time = None

        result = add_nurse_feed(DEMO_BABY_ID, record_date, start_time, end_time)
        message = "Add nurse feed result: {}".format(result)

    if intent == "addSolidFood":
        record_date = datetime.utcnow().strftime('%Y-%m-%d')
        time = slots["Time"]["value"]["interpretedValue"]
        if time == "now":
            time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        food_type = slots["Type"]["value"]["interpretedValue"]
        result = add_solid_food(DEMO_BABY_ID, record_date, time, food_type)
        message = "Add solid food result: {}".format(result)

    if intent == "addDiaperPee":
        record_date = datetime.utcnow().strftime('%Y-%m-%d')
        time = slots["Time"]["value"]["interpretedValue"]
        if time == "now":
            time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        result = add_diaper_pee(DEMO_BABY_ID, record_date, time)
        message = "Add diaper pee result: {}".format(result)

    if intent == "addDiaperPoo":
        record_date = datetime.utcnow().strftime('%Y-%m-%d')
        time = slots["Time"]["value"]["interpretedValue"]
        if time == "now":
            time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        result = add_diaper_poo(DEMO_BABY_ID, record_date, time)
        message = "Add diaper poo result: {}".format(result)

    if intent == "addBath":
        record_date = datetime.utcnow().strftime('%Y-%m-%d')
        time = slots["Time"]["value"]["interpretedValue"]
        if time == "now":
            time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        result = add_bath(DEMO_BABY_ID, record_date, time)
        message = "Add bath result: {}".format(result)

    if intent == "addMedicine":
        record_date = datetime.utcnow().strftime('%Y-%m-%d')
        time = slots["Time"]["value"]["interpretedValue"]
        if time == "now":
            time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        if "MedType" in slots and "value" in slots["MedType"]:
            med_type = slots["MedType"]["value"]["interpretedValue"]
        else:
            med_type = None
        result = add_medicine(DEMO_BABY_ID, record_date, time, med_type)
        message = "Add medicine result: {}".format(result)

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
    - addGrowthRecord(baby_id, record_date, height, weight, head_circumference)
    - addVaccineRecord(baby_id, record_date, vaccine_type)
    - addSleepRecord(baby_id, date, start_time, end_time)
    - addBottleFeed(baby_id, date, bottle_time, volume)
    - addNurseFeed(baby_id, date, start_time, end_time)
    - addSolidFood(baby_id, date, food_time, food_type)
    - addDiaperPee(baby_id, date, pee_time)
    - addDiaperPoo(baby_id, date, poo_time)
    - addBath(baby_id, date, bath_time)
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
    - updateMostRecentVaccineDate...
    
    
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

def dispatchTest(intent: str, slots: any):
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
                # "type": "Delegate"
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
                "content": "Howray! FulfillmentCodeHook!"
            }
        ]
    }

    return response

# def main(event, context):
#     print('request: {}'.format(json.dumps(event)))
#
#     intent = event["sessionState"]["intent"]["name"]
#     slots = event["sessionState"]["intent"]["slots"]
#
#     print(event["invocationSource"])
#     print(intent)
#     print(slots)
#
#     if event['invocationSource'] == 'DialogCodeHook':
#         response = delegate(intent, slots)
#
#     if event["invocationSource"] == "FulfillmentCodeHook":
#         response = dispatch(intent, slots)
#
#     return response

def lambda_handler(event: any, context: any):

    intent = event["sessionState"]["intent"]["name"]
    slots = event["sessionState"]["intent"]["slots"]

    print(event["invocationSource"])
    print(intent)
    print(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        response = delegate(intent, slots)

    if event["invocationSource"] == "FulfillmentCodeHook":
        response = dispatchTest(intent, slots)

    return response