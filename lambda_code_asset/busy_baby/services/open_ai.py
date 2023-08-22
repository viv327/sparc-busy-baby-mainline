import openai
import json
import boto3
from botocore.exceptions import ClientError


def _get_api_key():
    secret_name = "SparcBusyBaby"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    return json.loads(get_secret_value_response['SecretString'])


def get_openai_response(user_utterance):
    # First, retrieve API key from AWS Secret Manager and set it to openai API
    openai.api_key = _get_api_key()['openai']

    # Construct prompt
    messages = [
        {
            'role': 'system',
            'content': 'You are a kind helpful assistant.'
        },
        {
            'role': 'user',
            'content': 'Emma was born on 2020-01-01, gender female, height 85 cm, weight 28 pounds. The parent asks "{}?". Provide a concise answer.'.format(user_utterance)
        }
    ]

    # Invoke OpenAI API
    chat = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',  # default model
        messages=messages
    )
    reply = chat.choices[0].message.content
    print(f'ChatGPT: {reply}')
    return reply

