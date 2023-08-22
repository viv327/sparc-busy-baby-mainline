import openai
import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
from ..api import get_baby_profile, calculate_daily_sleep_time, calculate_daily_milk_volume


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


def _construct_prompt(baby_id, user_utterance):

    # retrieve baby_profile based on baby_id
    baby_profile = get_baby_profile(baby_id)

    daily_sleep_time = calculate_daily_sleep_time(baby_id)
    daily_milk_volume = calculate_daily_milk_volume(baby_id)

    today = datetime.utcnow().strftime("%Y-%m-%d")

    prompt_template = '''
        Today is {today}. {first_name} was born on {birthday}, gender {gender}, height {height} inches, weight {weight} pounds, sleeps {daily_sleep_time} per day, drinks {daily_milk_volume} ml milk per day.
        Provide a natural and concise answer to this question by the parent: {user_utterance}'''.format(
        today=today,
        first_name=baby_profile.first_name,
        birthday=baby_profile.birthday,
        gender=baby_profile.gender,
        height=baby_profile.height,
        weight=baby_profile.weight,
        daily_sleep_time=daily_sleep_time,
        daily_milk_volume=daily_milk_volume,
        user_utterance=user_utterance
    )
    return prompt_template


def get_openai_response(baby_id, user_utterance):
    # First, retrieve API key from AWS Secret Manager and set it to openai API
    openai.api_key = _get_api_key()['openai']

    # Construct prompt
    prompt = _construct_prompt(baby_id, user_utterance)
    print(prompt)

    messages = [
        {
            'role': 'system',
            'content': 'You are a kind helpful assistant.'
        },
        {
            'role': 'user',
            'content': _construct_prompt
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

