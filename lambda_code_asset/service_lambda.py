import json

from busy_baby.data_utils import create_baby


def dispatch(intent: str, slots: any):
    response = {}

    # dispatch to different service based on different intent
    if intent == "createBaby":
        response = create_baby(intent, slots)
    if intent == "createGrowthRecord":
        response = {}
    if intent == "createVaccineRecord":
        response = {}
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
