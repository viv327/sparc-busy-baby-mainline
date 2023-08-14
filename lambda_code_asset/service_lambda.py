import json


def main(event, context):
    print('request: {}'.format(json.dumps(event)))

    action_name = context['action_name']
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'This lambda will be the backend service for SparcBusyBaby application'
    }