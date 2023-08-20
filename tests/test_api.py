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
            baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02', "04:07")

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
            assert retrieved_item['Item']['delivery_time'] == {'S': '04:07'}

    def test_add_growth_record(self, ddb_client):
        with create_baby_profile_table(ddb_client):

            baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02', "04:07")

            # call API to put item in DDB table
            api.add_growth_record(baby_id, '2023-08-16', '40', '30', '20')

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

            baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02', "04:07")

            # call API to put item in DDB table
            api.add_vaccine_record(baby_id, '2023-08-16', 'DTaP', "memo")

            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=BABY_PROFILE_DDB_TABLE,
                Key={
                    "baby_id": {"S": DEMO_BABY_ID}
                }
            )

            assert retrieved_item['Item']['first_name'] == {'S': 'Emma'}
            assert retrieved_item['Item']['vaccine_record']['L'][0]['M']['record_date'] == {'S': '2023-08-16'}
            assert retrieved_item['Item']['vaccine_record']['L'][0]['M']['vaccine_type'] == {'S': 'DTaP'}
            assert retrieved_item['Item']['vaccine_record']['L'][0]['M']['vaccine_note'] == {'S': 'memo'}

    def test_add_sleep_record(self, ddb_client):
        with create_daily_record_table(ddb_client):

            # call API to put item in DDB table

            # api.add_sleep_record(DEMO_BABY_ID, '2020-02-02', '2023-08-16T19:22:36', '2023-08-16T19:52:36', "memo")

            api.add_sleep_record(DEMO_BABY_ID, '2020-02-02', '2023-08-16T19:22:36', None, "memo")
            api.add_sleep_record(DEMO_BABY_ID, '2020-02-02', None, '2023-08-16T19:52:36', "memo")


            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=DAILY_RECORD_DDB_TABLE,
                Key={
                    "baby_id": {"S": DEMO_BABY_ID},
                    "record_date": {"S": '2020-02-02'}
                }
            )

            assert retrieved_item['Item']['sleep_records']['L'][0]['M']['start_time'] == {'S': '2023-08-16T19:22:36'}
            assert retrieved_item['Item']['sleep_records']['L'][0]['M']['end_time'] == {'S': '2023-08-16T19:52:36'}
            assert retrieved_item['Item']['sleep_records']['L'][0]['M']['sleep_note'] == {'S': 'memo'}

    def test_add_bottle_feed(self, ddb_client):
        with create_daily_record_table(ddb_client):

            # baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02')

            # call API to put item in DDB table
            api.add_bottle_feed(DEMO_BABY_ID, '2020-02-02', '2023-08-16T19:22:36', 80, "memo")

            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=DAILY_RECORD_DDB_TABLE,
                Key={
                    "baby_id": {"S": DEMO_BABY_ID},
                    "record_date": {"S": '2020-02-02'}
                }
            )
            assert retrieved_item['Item']['bottle_feeds']['L'][0]['M']['time'] == {'S': '2023-08-16T19:22:36'}
            assert retrieved_item['Item']['bottle_feeds']['L'][0]['M']['volume'] == {'N': '80'}
            assert retrieved_item['Item']['bottle_feeds']['L'][0]['M']['formula_note'] == {'S': 'memo'}

    def test_add_nurse_feed(self, ddb_client):
        with create_daily_record_table(ddb_client):

            # call API to put item in DDB table

            api.add_nurse_feed(DEMO_BABY_ID, '2020-02-02', '2023-08-16T19:22:36', '2023-08-16T19:52:36', "memo")

            # api.add_nurse_feed(DEMO_BABY_ID, '2020-02-02', '2023-08-16T19:22:36', None)
            # api.add_nurse_feed(DEMO_BABY_ID, '2020-02-02', None, '2023-08-16T19:52:36')


            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=DAILY_RECORD_DDB_TABLE,
                Key={
                    "baby_id": {"S": DEMO_BABY_ID},
                    "record_date": {"S": '2020-02-02'}
                }
            )

            assert retrieved_item['Item']['nurse_feeds']['L'][0]['M']['start_time'] == {'S': '2023-08-16T19:22:36'}
            assert retrieved_item['Item']['nurse_feeds']['L'][0]['M']['end_time'] == {'S': '2023-08-16T19:52:36'}
            assert retrieved_item['Item']['nurse_feeds']['L'][0]['M']['nursing_note'] == {'S': 'memo'}

    def test_add_solid_food(self, ddb_client):
        with create_daily_record_table(ddb_client):

            # call API to put item in DDB table
            api.add_solid_food(DEMO_BABY_ID, '2020-02-02', '2023-08-16T19:22:36', "banana", "memo")

            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=DAILY_RECORD_DDB_TABLE,
                Key={
                    "baby_id": {"S": DEMO_BABY_ID},
                    "record_date": {"S": '2020-02-02'}
                }
            )
            assert retrieved_item['Item']['solid_foods']['L'][0]['M']['time'] == {'S': '2023-08-16T19:22:36'}
            assert retrieved_item['Item']['solid_foods']['L'][0]['M']['food_type'] == {'S': 'banana'}
            assert retrieved_item['Item']['solid_foods']['L'][0]['M']['food_note'] == {'S': 'memo'}

    def test_add_diaper_pee(self, ddb_client):
        with create_daily_record_table(ddb_client):

            # call API to put item in DDB table
            api.add_diaper_pee(DEMO_BABY_ID, '2020-02-02', '2023-08-16T19:22:36', "memo")

            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=DAILY_RECORD_DDB_TABLE,
                Key={
                    "baby_id": {"S": DEMO_BABY_ID},
                    "record_date": {"S": '2020-02-02'}
                }
            )
            assert retrieved_item['Item']['diaper_pees']['L'][0]['M']['time'] == {'S': '2023-08-16T19:22:36'}
            assert retrieved_item['Item']['diaper_pees']['L'][0]['M']['diaper_note'] == {'S': 'memo'}

    def test_add_diaper_poo(self, ddb_client):
        with create_daily_record_table(ddb_client):

            # call API to put item in DDB table
            api.add_diaper_poo(DEMO_BABY_ID, '2020-02-02', '2023-08-16T19:22:36', "memo")

            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=DAILY_RECORD_DDB_TABLE,
                Key={
                    "baby_id": {"S": DEMO_BABY_ID},
                    "record_date": {"S": '2020-02-02'}
                }
            )
            assert retrieved_item['Item']['diaper_poos']['L'][0]['M']['time'] == {'S': '2023-08-16T19:22:36'}
            assert retrieved_item['Item']['diaper_poos']['L'][0]['M']['diaper_note'] == {'S': 'memo'}
    def test_add_bath(self, ddb_client):
        with create_daily_record_table(ddb_client):

            # call API to put item in DDB table
            api.add_bath(DEMO_BABY_ID, '2020-02-02', '2023-08-17T19:22:36', "memo")

            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=DAILY_RECORD_DDB_TABLE,
                Key={
                    "baby_id": {"S": DEMO_BABY_ID},
                    "record_date": {"S": '2020-02-02'}
                }
            )
            assert retrieved_item['Item']['baths']['L'][0]['M']['time'] == {'S': '2023-08-17T19:22:36'}
            assert retrieved_item['Item']['baths']['L'][0]['M']['bath_note'] == {'S': 'memo'}

    def test_add_medicine(self, ddb_client):
        with create_daily_record_table(ddb_client):

            # call API to put item in DDB table
            api.add_medicine(DEMO_BABY_ID, '2020-02-02', '2023-08-17T19:22:36', 'Tylenol', "memo")

            # retrieve from DDB table by key
            retrieved_item = ddb_client.get_item(
                TableName=DAILY_RECORD_DDB_TABLE,
                Key={
                    "baby_id": {"S": DEMO_BABY_ID},
                    "record_date": {"S": '2020-02-02'}
                }
            )
            assert retrieved_item['Item']['medicines']['L'][0]['M']['time'] == {'S': '2023-08-17T19:22:36'}
            assert retrieved_item['Item']['medicines']['L'][0]['M']['med_type'] == {'S': 'Tylenol'}

            assert retrieved_item['Item']['medicines']['L'][0]['M']['med_note'] == {'S': 'memo'}

    def test_get_most_recent_height(self, ddb_client):
        with create_baby_profile_table(ddb_client):
            baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02', '2023-08-17T19:22:36')
            api.add_growth_record(DEMO_BABY_ID, '2023-08-16', '40', '30', '20')
            result = api.get_most_recent_height(DEMO_BABY_ID)
            assert result[0] == '40'
            assert result[1] == '2023-08-16'

    def test_get_most_recent_weight(self, ddb_client):
        with create_baby_profile_table(ddb_client):
            baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02', '2023-08-17T19:22:36')
            api.add_growth_record(DEMO_BABY_ID, '2023-08-16', '40', '30', '20')
            result = api.get_most_recent_weight(DEMO_BABY_ID)
            assert result[0] == '30'
            assert result[1] == '2023-08-16'

    def test_get_most_recent_head_circumference(self, ddb_client):
        with create_baby_profile_table(ddb_client):
            baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02', '2023-08-17T19:22:36')
            api.add_growth_record(DEMO_BABY_ID, '2023-08-16', '40', '30', '20')
            result = api.get_most_recent_head_circumference(DEMO_BABY_ID)
            assert result[0] == '20'
            assert result[1] == '2023-08-16'

    def test_get_most_recent_vaccine(self, ddb_client):
        with create_baby_profile_table(ddb_client):
            baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02', '2023-08-17T19:22:36')
            api.add_vaccine_record(DEMO_BABY_ID, '2023-08-16', 'DTaP', 'memo')
            api.add_vaccine_record(DEMO_BABY_ID, '2023-09-16', 'DTaP2', 'memo')
            result = api.get_most_recent_vaccine(DEMO_BABY_ID)
            assert result[0] == 'DTaP2'
            assert result[1] == '2023-09-16'

    def test_get_most_recent_sleep_start(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_sleep_record(DEMO_BABY_ID, '2023-08-16', '2023-08-17T19:22:36', '2023-08-17T20:52:36', None)
            result = api.get_most_recent_sleep_start(DEMO_BABY_ID, '2023-08-16')
            assert result == '07:22PM'

    def test_get_most_recent_sleep_end(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_sleep_record(DEMO_BABY_ID, '2023-08-16', '2023-08-17T19:22:36', '2023-08-17T20:52:36', None)
            result = api.get_most_recent_sleep_end(DEMO_BABY_ID, '2023-08-16')
            assert result == '08:52PM'

    def test_get_most_recent_sleep_duration(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_sleep_record(DEMO_BABY_ID, '2023-08-17', '2023-08-17T19:22:36', '2023-08-17T20:52:38', None)
            result = api.get_most_recent_sleep_duration(DEMO_BABY_ID, '2023-08-17')
            assert result == '1 hour 30 minutes'

    def test_total_sleep_time(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_sleep_record(DEMO_BABY_ID, '2023-08-17', '2023-08-17T9:22:36', '2023-08-17T10:52:38', None)
            api.add_sleep_record(DEMO_BABY_ID, '2023-08-17', '2023-08-17T19:22:36', '2023-08-17T20:42:38', None)
            result = api.get_total_sleep_time(DEMO_BABY_ID, '2023-08-17')
            assert result == '2 hours 50 minutes'

    def test_total_sleep_count(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_sleep_record(DEMO_BABY_ID, '2023-08-17', '2023-08-17T9:22:36', '2023-08-17T10:52:38', None)
            api.add_sleep_record(DEMO_BABY_ID, '2023-08-17', '2023-08-17T19:22:36', '2023-08-17T20:42:38', None)
            api.add_sleep_record(DEMO_BABY_ID, '2023-08-17', '2023-08-17T19:22:36', None, None)
            result = api.get_total_sleep_count(DEMO_BABY_ID, '2023-08-17')
            assert result == '2'

    def test_get_most_recent_bottle_feed(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_bottle_feed(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:22:36', '80', None)
            result = api.get_most_recent_bottle_feed(DEMO_BABY_ID, '2023-08-16')
            assert result[0] == '80'
            assert result[1] == '07:22PM'

    def test_total_bottle_feed_volume(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_bottle_feed(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:22:36', '60', None)
            api.add_bottle_feed(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:22:36', '80', None)
            result = api.get_total_bottle_feed_volume(DEMO_BABY_ID, '2023-08-16')
            assert result == '140'

    def test_total_bottle_feed_count(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_bottle_feed(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:22:36', '60', None)
            api.add_bottle_feed(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:22:36', '80', None)
            result = api.get_total_bottle_feed_count(DEMO_BABY_ID, '2023-08-16')
            assert result == '2'

    def test_get_most_recent_nurse_feed_end(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_nurse_feed(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:22:36', '2023-08-16T19:52:36', None)
            result = api.get_most_recent_nurse_feed_end(DEMO_BABY_ID, '2023-08-16')
            assert result == '07:52PM'

    def test_total_nurse_feed_count(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_nurse_feed(DEMO_BABY_ID, '2023-08-17', '2023-08-17T9:22:36', '2023-08-17T9:52:38', None)
            api.add_nurse_feed(DEMO_BABY_ID, '2023-08-17', '2023-08-17T19:22:36', '2023-08-17T19:42:38', None)
            api.add_nurse_feed(DEMO_BABY_ID, '2023-08-17', '2023-08-17T19:22:36', None, None)
            result = api.get_total_nurse_feed_count(DEMO_BABY_ID, '2023-08-17')
            assert result == '2'

    def test_get_most_recent_solid_food(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_solid_food(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:28:36', 'banana', None)
            result = api.get_most_recent_solid_food(DEMO_BABY_ID, '2023-08-16')
            assert result[0] == 'banana'
            assert result[1] == '07:28PM'

    def test_get_total_solid_food_count(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_solid_food(DEMO_BABY_ID, '2023-08-16', '2023-08-16T09:28:36', 'banana', None)
            api.add_solid_food(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:28:36', 'banana', None)
            api.add_solid_food(DEMO_BABY_ID, '2023-08-16', '2023-08-16T21:28:36', 'avocado', None)
            result = api.get_total_solid_food_count(DEMO_BABY_ID, '2023-08-16')
            assert result == '3'

    def test_get_all_solid_food_types(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_solid_food(DEMO_BABY_ID, '2023-08-16', '2023-08-16T09:28:36', 'banana', None)
            api.add_solid_food(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:28:36', 'banana', None)
            api.add_solid_food(DEMO_BABY_ID, '2023-08-16', '2023-08-16T21:28:36', 'avocado', None)
            result = api.get_all_solid_food_types(DEMO_BABY_ID, '2023-08-16')
            assert result == {'banana', 'avocado'}

    def test_get_most_recent_diaper_pee(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_diaper_pee(DEMO_BABY_ID, '2023-08-16', '2023-08-16T07:28:36', None)
            result = api.get_most_recent_diaper_pee(DEMO_BABY_ID, '2023-08-16')
            assert result == '07:28AM'

    def test_get_total_diaper_pee_count(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_diaper_pee(DEMO_BABY_ID, '2023-08-16', '2023-08-16T09:28:36', None)
            api.add_diaper_pee(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:28:36', None)
            api.add_diaper_pee(DEMO_BABY_ID, '2023-08-16', '2023-08-16T21:28:36', None)
            result = api.get_total_diaper_pee_count(DEMO_BABY_ID, '2023-08-16')
            assert result == '3'

    def test_get_most_recent_diaper_poo(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_diaper_poo(DEMO_BABY_ID, '2023-08-16', '2023-08-16T07:28:36', None)
            api.add_diaper_poo(DEMO_BABY_ID, '2023-08-16', '2023-08-16T09:28:36', None)
            result = api.get_most_recent_diaper_poo(DEMO_BABY_ID, '2023-08-16')
            assert result == '09:28AM'

    def test_get_total_diaper_poo_count(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_diaper_poo(DEMO_BABY_ID, '2023-08-16', '2023-08-16T09:28:36', None)
            api.add_diaper_poo(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:28:36', None)
            result = api.get_total_diaper_poo_count(DEMO_BABY_ID, '2023-08-16')
            assert result == '2'

    def test_get_most_recent_bath(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_bath(DEMO_BABY_ID, '2023-08-16', '2023-08-16T07:29:36', None)
            result = api.get_most_recent_bath(DEMO_BABY_ID, '2023-08-16')
            assert result == '07:29AM'

    def test_get_most_recent_medicine(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_medicine(DEMO_BABY_ID, '2023-08-16', '2023-08-16T07:29:36', 'Tylenol', None)
            result = api.get_most_recent_medicine(DEMO_BABY_ID, '2023-08-16')
            assert result[0] == 'Tylenol'
            assert result[1] == '07:29AM'

    def test_get_total_medicine_count(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_medicine(DEMO_BABY_ID, '2023-08-16', '2023-08-16T09:28:36', 'Tylenol', None)
            api.add_medicine(DEMO_BABY_ID, '2023-08-16', '2023-08-16T19:28:36', 'Tylenol', None)
            result = api.get_total_medicine_count(DEMO_BABY_ID, '2023-08-16')
            assert result == '2'

    def test_delete_most_recent_sleep_record(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_sleep_record(DEMO_BABY_ID, '2023-08-17', '2023-08-17T19:22:36', '2023-08-17T20:52:38', None)
            # api.add_sleep_record(DEMO_BABY_ID, '2023-08-17', '2023-08-17T20:22:36', '2023-08-17T21:52:38', None)
            api.delete_most_recent_sleep_record(DEMO_BABY_ID, '2023-08-17')
            # result = api.get_most_recent_sleep_end(DEMO_BABY_ID, '2023-08-17')
            # assert result == '08:52PM'
            result = api.get_total_sleep_count(DEMO_BABY_ID, '2023-08-17')
            assert result == "0"

    def test_update_most_recent_vaccine_date(self, ddb_client):
        with create_baby_profile_table(ddb_client):
            baby_id = api.create_baby('Emma', 'Li', 'Female', '2020-02-02', '2023-08-17T19:22:36')
            api.add_vaccine_record(DEMO_BABY_ID, '2023-08-17', 'DTaP', None)
            api.add_vaccine_record(DEMO_BABY_ID, '2023-08-18', 'DTaP2', None)
            api.update_most_recent_vaccine_date(DEMO_BABY_ID, '2023-08-19')
            result = api.get_most_recent_vaccine(DEMO_BABY_ID)
            assert result[1] == '2023-08-19'

    def test_update_most_recent_sleep_record(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_sleep_record(DEMO_BABY_ID, '2023-08-17', '2023-08-17T19:22:36', '2023-08-17T20:52:38', None)
            api.add_sleep_record(DEMO_BABY_ID, '2023-08-17', '2023-08-17T20:22:36', '2023-08-17T21:52:38', None)
            api.update_most_recent_sleep_record(DEMO_BABY_ID, '2023-08-17', '2023-08-17T20:30:36', None)
            result = api.get_most_recent_sleep_start(DEMO_BABY_ID, '2023-08-17')
            assert result == '08:30PM'
            api.update_most_recent_sleep_record(DEMO_BABY_ID, '2023-08-17', None, '2023-08-17T21:50:38')
            result = api.get_most_recent_sleep_end(DEMO_BABY_ID, '2023-08-17')
            assert result == '09:50PM'

    def test_update_most_recent_bottle_feed(self, ddb_client):
        with create_daily_record_table(ddb_client):
            api.add_bottle_feed(DEMO_BABY_ID, '2023-08-17', '2023-08-17T19:22:36', '80', None)
            api.add_bottle_feed(DEMO_BABY_ID, '2023-08-17', '2023-08-17T19:22:36', '60', None)
            api.update_most_recent_bottle_feed(DEMO_BABY_ID, '2023-08-17', '40')
            result = api.get_most_recent_bottle_feed(DEMO_BABY_ID, '2023-08-17')
            assert result[0] == '40'

