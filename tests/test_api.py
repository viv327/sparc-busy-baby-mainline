from contextlib import contextmanager

import pytest

from lambda_code_asset.busy_baby.constants import BABY_PROFILE_DDB_TABLE, DAILY_RECORD_DDB_TABLE, DEMO_BABY_ID
from lambda_code_asset.busy_baby import api


@contextmanager
def create_baby_profile_table(dynamodb_client):
    """Create mock baby profile DynamoDB table"""

    dynamodb_client.create_table(
        TableName=BABY_PROFILE_DDB_TABLE,
        KeySchema=[
            {
                'AttributeName': 'baby_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'baby_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    yield


@contextmanager
def create_daily_record_table(dynamodb_client):
    """Create mock daily record DynamoDB table"""

    dynamodb_client.create_table(
        TableName=DAILY_RECORD_DDB_TABLE,
        KeySchema=[
            {
                'AttributeName': 'baby_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'record_date',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'baby_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'record_date',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    yield


"""
Below is the main test class to test APIs
To run the tests, simply run "pytest" in terminal
"""


class TestAPI:
    """
    Make sure all test methods are prefixed with "test_"
    """
    def test_create_baby_profile_table(self, ddb_client):
        """Test creation of 'baby_profile' DynamoDB table"""

        with create_baby_profile_table(ddb_client):
            res = ddb_client.describe_table(TableName=BABY_PROFILE_DDB_TABLE)
            res2 = ddb_client.list_tables()

            assert res['Table']['TableName'] == BABY_PROFILE_DDB_TABLE
            assert res2['TableNames'] == [BABY_PROFILE_DDB_TABLE]

    def test_put_sleep_record(self, ddb_client):
        """Test adding an item to 'daily_record' DynamoDB table"""

        with create_daily_record_table(ddb_client):
            add_item = ddb_client.put_item(
                TableName=DAILY_RECORD_DDB_TABLE,
                Item={
                    "baby_id": {"S": "001"},
                    "record_date": {"S": "2020-01-01"},
                },
            )

            res = ddb_client.get_item(
                TableName=DAILY_RECORD_DDB_TABLE,
                Key={
                    "baby_id": {"S": "001"},
                    "record_date": {"S": "2020-01-01"},
                },
            )

            assert add_item['ResponseMetadata']['HTTPStatusCode'] == 200
            assert res['Item']['baby_id'] == {"S": "001"}
            assert len(res['Item']) == 2

    """
    Example test
    """
    def test_create_baby_profile(self, ddb_client):
        with create_baby_profile_table(ddb_client):
            # call API to put item in DDB table
            baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02')

            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=BABY_PROFILE_DDB_TABLE,
                Key={
                    "baby_id": {"S": baby_id}
                }
            )

            # assert
            assert retrieved_item['Item']['first_name'] == {'S': 'Emma'}
            assert retrieved_item['Item']['last_name'] == {'S': 'Li'}
            assert retrieved_item['Item']['gender'] == {'S': 'Female'}
            assert retrieved_item['Item']['birthday'] == {'S': '2020-02-02'}

    def test_add_growth_record(self, ddb_client):
        with create_baby_profile_table(ddb_client):

            baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02')

            # call API to put item in DDB table
            api.add_growth_record(baby_id, '2023-08-16T19:22:36', '40', '30', '20')

            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=BABY_PROFILE_DDB_TABLE,
                Key={
                    "baby_id": {"S": DEMO_BABY_ID}
                }
            )

            # assert

            # add this line to the breakpoint position, run "pytest" in terminal and debug there
            # to exit debug mode in terminal, type "exit()" -> ENTER
            # pytest.set_trace()

            assert retrieved_item['Item']['first_name'] == {'S': 'Emma'}
            assert retrieved_item['Item']['growth_record']['L'][0]['M']['height'] == {'S': '40'}
            # assert retrieved_item['Item']['last_name'] == {'S': 'Li'}
            # assert retrieved_item['Item']['gender'] == {'S': 'Female'}
            # assert retrieved_item['Item']['birthday'] == {'S': '2020-02-02'}

    def test_add_vaccine_record(self, ddb_client):
        with create_baby_profile_table(ddb_client):

            baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02')

            # call API to put item in DDB table
            api.add_vaccine_record(baby_id, '2023-08-16T19:22:36', 'DTaP')

            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=BABY_PROFILE_DDB_TABLE,
                Key={
                    "baby_id": {"S": DEMO_BABY_ID}
                }
            )

            assert retrieved_item['Item']['first_name'] == {'S': 'Emma'}
            assert retrieved_item['Item']['vaccine_record']['L'][0]['M']['vaccine_type'] == {'S': 'DTaP'}

    def test_add_bottle_feed(self, ddb_client):
        with create_daily_record_table(ddb_client):

            # baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02')

            # call API to put item in DDB table
            api.add_bottle_feed(DEMO_BABY_ID, '2020-02-02', '2023-08-16T19:22:36', 80)

            # # retrieve from DDB table by key
            # retrieved_item = ddb_client.get_item(
            #     TableName=DAILY_RECORD_DDB_TABLE,
            #     Key={
            #         "baby_id": {"S": DEMO_BABY_ID}
            #     }
            # )
            #
            # # assert retrieved_item['Item']['first_name'] == {'S': 'Emma'}
            # assert retrieved_item['Item']['bottle_feeds']['L'][0]['M']['volume'] == {'S': '80'}

            assert True == True