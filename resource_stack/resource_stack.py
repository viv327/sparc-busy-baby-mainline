from aws_cdk import (
    Stack,
    aws_lambda as function_lambda,
    aws_s3 as s3
)
from constructs import Construct


class ResourceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # main service Lambda
        function = function_lambda.Function(self,
                                            "SparcBusyBabyService",
                                            function_name="SparcBusyBabyService",
                                            runtime=function_lambda.Runtime.PYTHON_3_9,
                                            code=function_lambda.Code.from_asset('./lambda_code_asset'),
                                            handler="service_lambda.main")

        # S3 bucket
        bucket = s3.Bucket(self, "SparcBusyBabyBucket", versioned=True,
                           bucket_name="demo-bucket-for-sparc-aws-code-deploy",
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL)