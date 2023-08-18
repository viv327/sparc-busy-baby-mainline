import json
from datetime import datetime

from busy_baby.api import create_baby, add_growth_record, add_vaccine_record, add_bottle_feed, add_sleep_record, \
    add_nurse_feed, add_solid_food, add_diaper_pee, add_diaper_poo, add_bath, add_medicine
from busy_baby.constants import DEMO_BABY_ID, CREATE_BABY_INTENT, FIRST_NAME, LAST_NAME, GENDER, BIRTHDAY

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