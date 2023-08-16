import json
from datetime import datetime
from busy_baby.data_utils import create_baby, add_growth_record
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
        record_datetime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

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

    if intent == "createVaccineRecord":
        result = {}

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
    - addGrowthRecord
    - addSleepRecord
    - addBottleFeed(baby_id, datetime, volume)
    - addNurseFeed
    - addSolidFood
    - addDiaperPee
    - addDiaperPoo
    - addBath
    - addVaccine
    - addMedicine
    - getMostRecentSleepStart
    - getMostRecentSleepEnd
    - getMostRecentSleepDuration
    - getTotalSleepTime
    - getSleepCount
    - getMostRecentBottleFeedTime
    - getMostRecentBottleFeedVolume
    - getTotalBottleFeedVolume
    - getTotalBottleFeedCount
    - getMostRecentNurseFeedEnd
    - getTotalNurseFeedCount
    - getMostRecentSolidFoodTime
    - getMostRecentSolidFoodType
    - getTotalSolidFoodCount
    - getAllSolidFoodTypes
    - getMostRecentDiaperPeeTime
    - getTotalDiaperPeeCount
    - getMostRecentDiaperPooTime
    - getTotalDiaperPooCount
    - getMostRecentBathDay
    - getMostRecentVaccineDay
    - getAllVaccineTypes
    - getMostRecentMedicineTime
    - getTotalMedicineCount
    - deleteMostRecentSleepRecord
    - updateMostRecentSleepRecord
    - updateMostRecentBottleFeedVolume
    
    
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
