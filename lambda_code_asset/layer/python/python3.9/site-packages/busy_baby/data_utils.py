import boto3
import os
from constants import BABY_PROFILE_DDB_TABLE


def put_baby(slots: any):
    # Create a DynamoDB client
    dynamodb = boto3.resource("dynamodb")
    table_name = BABY_PROFILE_DDB_TABLE
    table = dynamodb.Table(table_name)
    user = os.environ["USER_NAME"]

    # # Check if user exists
    # get_response = table.get_item(
    #     Key={
    #         "baby_id": user,
    #         "BabyName": slots["FirstName"]["value"]["interpretedValue"]
    #     }
    # )
    #
    # # if exists, get current user
    # if "Item" in get_response:
    #     item = get_response["Item"]
    # # otherwise create a new item profile
    # else:
    #     item = {
    #         "User": user,
    #         "BabyName": slots["FirstName"]["value"]["interpretedValue"]
    #     }
    #
    # # Generate item
    # # get baby basic info from slots
    # item["DataType"] = "BabyProfile"
    # item["FirstName"] = slots["FirstName"]["value"]["interpretedValue"]
    # item["LastName"] = slots["LastName"]["value"]["interpretedValue"]
    # item["Gender"] = slots["Gender"]["value"]["interpretedValue"]
    # item["Birthday"] = slots["Birthday"]["value"]["interpretedValue"]
    # item["DeliveryTime"] = slots["DeliveryTime"]["value"]["interpretedValue"]
    #
    # # Add item to database
    # table.put_item(Item=item)

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
