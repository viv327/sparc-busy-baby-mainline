import os
import subprocess

import aws_cdk
from aws_cdk import (
    Stack,
    aws_iam,
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

        _external_dependency_layer = self.create_dependencies_layer("SparcBusyBabyService")

        function = aws_lambda.Function(self,
                                       "SparcBusyBabyService",
                                       function_name="SparcBusyBabyService",
                                       runtime=aws_lambda.Runtime.PYTHON_3_9,
                                       layers=[_lambda_layer, _external_dependency_layer],
                                       code=aws_lambda.Code.from_asset('./lambda_code_asset'),
                                       handler="service_lambda.main",
                                       timeout=aws_cdk.Duration.minutes(1))

        # Grant S3 full access to Lambda role (so that it can create bucket/object etc)
        s3_full_access = aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
        function.role.add_managed_policy(s3_full_access)

        # Grant permission for AWS Secret Manager
        policy = aws_iam.PolicyStatement(
            actions=[
                "secretsmanager:GetSecretValue",
                "secretsmanager:DescribeSecret",
                "secretsmanager:ListSecrets"
            ],
            resources=["*"])
        function.add_to_role_policy(policy)

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

    def create_dependencies_layer(self, function_name):
        requirements_file = "lambda_code_asset/lambda_dependencies/requirements.txt"
        output_dir = ".lambda_dependencies/" + function_name

        # Install requirements for layer in the output_dir
        if not os.environ.get("SKIP_PIP"):
            # Note: Pip will create the output dir if it does not exist
            subprocess.check_call(
                f"pip install -r {requirements_file} -t {output_dir}/python".split()
            )
        return aws_lambda.LayerVersion(
            self,
            function_name + "-dependencies",
            code=aws_lambda.Code.from_asset(output_dir)
        )
