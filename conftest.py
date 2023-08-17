import os
import boto3
import pytest

from moto import mock_dynamodb


# https://towardsdatascience.com/moto-pytest-and-aws-databases-a-quality-and-data-engineering-crossroads-ae58f9e7b265


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def ddb_client(aws_credentials):
    """DynamoDB mock client."""
    with mock_dynamodb():
        conn = boto3.client("dynamodb", region_name="us-east-1")
        yield conn
