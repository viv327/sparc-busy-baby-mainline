import boto3
import os
import uuid
from .constants import BABY_PROFILE_DDB_TABLE
from .basic_info import BabyProfile


def put_baby(slots: any):
    # Create a DynamoDB client
    dynamodb = boto3.resource("dynamodb")
    table_name = BABY_PROFILE_DDB_TABLE
    table = dynamodb.Table(table_name)

    # # Check if user exists
    # get_response = table.get_item(
    #     Key={
    #         "baby_id": slots["BabyId"]["value"]["interpretedValue"],
    #     }
    # )

    # # if exists, get current user
    # if "Item" in get_response:
    #     item = get_response["Item"]
    # # otherwise create a new item profile
    # else:
    #     # item = {
    #     #     "BabyId": slots["BabyId"]["value"]["interpretedValue"]
    #     # }
    #     item = {
    #         "baby_id": str(uuid.uuid4())
    #     }

    item = {"baby_id": str(uuid.uuid4()), "first_name": slots["FirstName"]["value"]["interpretedValue"],
            "last_name": slots["LastName"]["value"]["interpretedValue"],
            "gender": slots["Gender"]["value"]["interpretedValue"],
            "birthday": slots["Birthday"]["value"]["interpretedValue"]}

    # Generate item
    # get baby basic info from slots
    # item["DataType"] = "BabyProfile"
    # item["first_name"] = slots["FirstName"]["value"]["interpretedValue"]
    # item["LastName"] = slots["LastName"]["value"]["interpretedValue"]
    # item["Gender"] = slots["Gender"]["value"]["interpretedValue"]
    # item["Birthday"] = slots["Birthday"]["value"]["interpretedValue"]
    # item["DeliveryTime"] = slots["DeliveryTime"]["value"]["interpretedValue"]
    #
    # # Add item to database
    # table.put_item(Item=item)

    # Add item to database
    table.put_item(Item=item)

    print("Dummy: success!")


def create_baby(intent: str, slots: any):
    # Add data to dynamoDB
    put_baby(slots)

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
                "content": "Howray! FulfillmentCodeHook!"
            }
        ]
    }

    return response
