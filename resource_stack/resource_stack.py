from aws_cdk import (
    BundlingOptions,
    Stack,
    aws_lambda,
    aws_s3,
    aws_dynamodb
)
from constructs import Construct


class ResourceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # main service Lambda
        _lambda_layer = aws_lambda.LayerVersion(
            self, "Boto3LambdaLayer",
            code=aws_lambda.Code.from_asset('./lambda_code_asset/busy_baby'),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_9]
        )

        function = aws_lambda.Function(self,
                                       "SparcBusyBabyService",
                                       function_name="SparcBusyBabyService",
                                       runtime=aws_lambda.Runtime.PYTHON_3_9,
                                       layers=[_lambda_layer],
                                       code=aws_lambda.Code.from_asset(
                                           './lambda_code_asset',
                                           bundling=BundlingOptions(
                                               image=aws_lambda.Runtime.PYTHON_3_9.bundling_image,
                                               command=[
                                                   "bash", "-c",
                                                   "pip install --no-cache -r requirements.txt -t /asset-output && cp -au . /asset-output"
                                               ],
                                           )
                                       ),
                                       handler="service_lambda.main")

        # S3 bucket
        bucket = aws_s3.Bucket(self, "SparcBusyBabyBucket", versioned=True,
                               bucket_name="demo-bucket-for-sparc-aws-code-deploy",
                               block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL)

        # DynamoDB
        daily_record_table = aws_dynamodb.Table(self, "SparcBusyBabyDailyRecord",
                                                table_name="SparcBusyBabyDailyRecord",
                                                partition_key=aws_dynamodb.Attribute(
                                                    name="baby_id",
                                                    type=aws_dynamodb.AttributeType.STRING
                                                ),
                                                sort_key=aws_dynamodb.Attribute(
                                                    name="record_date",
                                                    type=aws_dynamodb.AttributeType.STRING
                                                )
                                                )
        daily_record_table.grant_read_write_data(function.role)

        baby_profile_table = aws_dynamodb.Table(self, "SparcBusyBabyProfile",
                                                table_name="SparcBusyBabyProfile",
                                                partition_key=aws_dynamodb.Attribute(
                                                    name="baby_id",
                                                    type=aws_dynamodb.AttributeType.STRING
                                                )
                                                )
        baby_profile_table.grant_read_write_data(function.role)
