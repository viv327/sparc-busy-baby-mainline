import aws_cdk as core
import aws_cdk.assertions as assertions

from sparc_busy_baby_mainline.sparc_busy_baby_mainline_stack import SparcBusyBabyMainlineStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sparc_busy_baby_mainline/sparc_busy_baby_mainline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SparcBusyBabyMainlineStack(app, "sparc-busy-baby-mainline")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
