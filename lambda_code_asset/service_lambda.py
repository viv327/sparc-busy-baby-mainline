import json

from busy_baby.data_utils import create_baby


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

    if intent == "createGrowthRecord":
        result = {}
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
