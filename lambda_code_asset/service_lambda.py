import json
from datetime import datetime

import dateutil.tz
import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir


from busy_baby.api import create_baby, add_growth_record, add_vaccine_record, add_bottle_feed, add_sleep_record, \
    add_nurse_feed, add_solid_food, add_diaper_pee, add_diaper_poo, add_bath, add_medicine, get_most_recent_height, \
    get_most_recent_weight, get_most_recent_head_circumference, get_most_recent_vaccine, get_most_recent_sleep_start, \
    get_most_recent_sleep_end, get_most_recent_sleep_duration, get_total_sleep_time, get_total_sleep_count, \
    get_most_recent_bottle_feed, get_total_bottle_feed_volume, get_total_bottle_feed_count, get_most_recent_nurse_feed_end, \
    get_total_nurse_feed_count, get_most_recent_solid_food, get_total_solid_food_count, get_all_solid_food_types, \
    get_most_recent_diaper_pee, get_total_diaper_pee_count, get_most_recent_diaper_poo, get_total_diaper_poo_count, \
    get_most_recent_bath, get_most_recent_medicine, get_total_medicine_count, delete_most_recent_sleep_record, \
    update_most_recent_vaccine_date, update_most_recent_sleep_record, update_most_recent_bottle_feed
from busy_baby.constants import DEMO_BABY_ID, FIRST_NAME, LAST_NAME, GENDER, BIRTHDAY, ADD_BABY, ADD_GROWTH, \
    ADD_VACCINE, ADD_SLEEP, ADD_FORMULA, ADD_NURSING, ADD_FOOD, ADD_BATH, ADD_MEDICATION, DELIVERY_TIME, GROWTH_DATE, \
    GROWTH_TYPE, GROWTH_DATA, VACCINE_DATE, VACCINE_TYPE, SLEEP_TIME, START_END, FORMULA_TIME, FORMULA_VOLUME, \
    NURSING_TIME, FOOD_TIME, FOOD_TYPE, ADD_DIAPER, DIAPER_TYPE, DIAPER_TIME, BATH_TIME, MED_TIME, MED_TYPE, SLEEP_DATE, \
    FORMULA_DATE, NURSING_DATE, FOOD_DATE, DIAPER_DATE, BATH_DATE, MED_DATE, MED_NOTE, BATH_NOTE, DIAPER_NOTE, \
    FOOD_NOTE, NURSING_NOTE, FORMULA_NOTE, SLEEP_NOTE, VACCINE_NOTE, GET_RECORD, RECORD_TYPE, RECORD_DATE, \
    DELETE_RECORD, DELETE_TYPE, UPDATE_RECORD, UPDATE_TYPE, ENABLE_PREMIUM_FEATURE, USER_ASSET_S3_BUCKET_NAME, \
    UPDATE_DATE, UPDATE_TIME, UPDATE_DATA, CONSULT_AI, CONSULT
from busy_baby.utils import format_timedelta
from busy_baby.services.open_ai import get_openai_response


def dispatch(intent: str, slots: any):
    def getSlotVal(slotName):
        return slots[slotName]["value"]["interpretedValue"] if slotName in slots else None

    response = {}
    message = ''
    timeZone = dateutil.tz.gettz('US/Eastern')

    # dispatch to different service based on different intent

    if intent == ADD_BABY:
        first_name = getSlotVal(FIRST_NAME)
        last_name = getSlotVal(LAST_NAME)
        gender = getSlotVal(GENDER)
        birthday = getSlotVal(BIRTHDAY)
        delivery_time = getSlotVal(DELIVERY_TIME)
        delivery_time = datetime.strptime(birthday + " " + delivery_time, "%Y-%m-%d %H:%M").isoformat()

        result = create_baby(first_name, last_name, gender, birthday, delivery_time)
        message = "Baby profile creation result: {}".format(result)

    if intent == ADD_GROWTH:
        record_date = slots[GROWTH_DATE]["value"]["interpretedValue"]

        # create_growth_record only takes 3 slots, date, category and measured data.
        # might be different from the database schema
        growth_type = getSlotVal(GROWTH_TYPE)
        growth_data = getSlotVal(GROWTH_DATA)

        height = growth_data if growth_type == "height" else None
        weight = growth_data if growth_type == "weight" else None
        head_circumference = growth_data if growth_type == "head circumference" else None

        result = add_growth_record(DEMO_BABY_ID, record_date, height, weight, head_circumference)
        message = "Update baby growth record result: {}".format(result)

    if intent == ADD_VACCINE:
        record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(VACCINE_DATE) == "today" else getSlotVal(VACCINE_DATE) # convert current UTC date to strings

        vaccine_type = getSlotVal(VACCINE_TYPE)
        vaccine_note = getSlotVal(VACCINE_NOTE)
        result = add_vaccine_record(DEMO_BABY_ID, record_date, vaccine_type, vaccine_note)
        message = "Update baby vaccine record result: {}".format(result)

    if intent == ADD_SLEEP:
        # record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(SLEEP_DATE) == "today" else getSlotVal(SLEEP_DATE)

        record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(SLEEP_DATE) == "today" else getSlotVal(SLEEP_DATE)

        # intent takes a slot "start_end" which lets user decide if the current record is a start or end time point, then enter the time in slot "sleep time"
        # not in to two slots as "start_time"/"end_time"
        sleep_time = getSlotVal(SLEEP_TIME)
        # sleep_time_format = format_date_and_time(record_date, sleep_time)
        sleep_time = datetime.strptime(record_date + " " + sleep_time, "%Y-%m-%d %H:%M").isoformat()
        start_end = getSlotVal(START_END)
        sleep_note = getSlotVal(SLEEP_NOTE)

        start_time = sleep_time if start_end == "start" else None
        end_time = sleep_time if start_end == "finish" else None

        result = add_sleep_record(DEMO_BABY_ID, record_date, start_time, end_time, sleep_note)
        message = "Add sleep record result: {}".format(result)
        # message = "Thanks for confirming. We have taken the sleep record! Have a nice dream."

    if intent == ADD_FORMULA:
        record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(FORMULA_DATE) == "today" else getSlotVal(FORMULA_DATE)

        # in current bot design, we only manually set value for date, no such operation for time "now".
        # so if else only needed for date, not for time, as in the current design.
        formula_time = getSlotVal(FORMULA_TIME)
        formula_time = datetime.strptime(record_date + " " + formula_time, "%Y-%m-%d %H:%M").isoformat()
        formula_volume = slots[FORMULA_VOLUME]["subSlots"]["growth_data"]["value"]["interpretedValue"]
        formula_note = getSlotVal(FORMULA_NOTE)
        result = add_bottle_feed(DEMO_BABY_ID, record_date, formula_time, formula_volume, formula_note)
        message = "Add bottle feed result: {}".format(result)

    if intent == ADD_NURSING:
        record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(NURSING_DATE) == "today" else getSlotVal(NURSING_DATE)

        nursing_time = getSlotVal(NURSING_TIME)
        nursing_time = datetime.strptime(record_date + " " + nursing_time, "%Y-%m-%d %H:%M").isoformat()
        nursing_note = getSlotVal(NURSING_NOTE)
        start_end = getSlotVal(START_END)

        start_time = nursing_time if start_end == "start" else None
        end_time = nursing_time if start_end == "finish" else None

        result = add_nurse_feed(DEMO_BABY_ID, record_date, start_time, end_time, nursing_note)
        message = "Add nurse feed result: {}".format(result)

    if intent == ADD_FOOD:
        record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(FOOD_DATE) == "today" else getSlotVal(FOOD_DATE)
        food_time = getSlotVal(FOOD_TIME)
        food_time = datetime.strptime(record_date + " " + food_time, "%Y-%m-%d %H:%M").isoformat()
        food_note = getSlotVal(FOOD_NOTE)
        # food_time = datetime.now(tz=timeZone).strftime('%Y-%m-%dT%H:%M:%S') if getSlotVal(FOOD_TIME)=="now" else getSlotVal(FOOD_TIME)
        food_type = getSlotVal(FOOD_TYPE)
        result = add_solid_food(DEMO_BABY_ID, record_date, food_time, food_type, food_note)
        message = "Add solid food result: {}".format(result)

    if intent == ADD_DIAPER:
        diaper_type = getSlotVal(DIAPER_TYPE)
        record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(DIAPER_DATE) == "today" else getSlotVal(DIAPER_DATE)
        diaper_time = getSlotVal(DIAPER_TIME)
        diaper_time = datetime.strptime(record_date + " " + diaper_time, "%Y-%m-%d %H:%M").isoformat()
        diaper_note = getSlotVal(DIAPER_NOTE)
        # diaper_time = datetime.now(tz=timeZone).strftime('%Y-%m-%dT%H:%M:%S') if getSlotVal(DIAPER_TIME) == "now" else getSlotVal(DIAPER_TIME)
        result = add_diaper_poo(DEMO_BABY_ID, record_date, diaper_time, diaper_note) if diaper_type == "poo" else add_diaper_pee(DEMO_BABY_ID, record_date, diaper_time, diaper_note)
        message = "Add diaper {} result: {}".format(diaper_type, result)

    if intent == ADD_BATH:
        record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(BATH_DATE) == "today" else getSlotVal(BATH_DATE)
        bath_time = getSlotVal(BATH_TIME)
        bath_time = datetime.strptime(record_date + " " + bath_time, "%Y-%m-%d %H:%M").isoformat()
        bath_note = getSlotVal(BATH_NOTE)
        # bath_time = datetime.now(tz=timeZone).strftime('%Y-%m-%dT%H:%M:%S') if getSlotVal(BATH_TIME) == "now" else getSlotVal(BATH_TIME)
        result = add_bath(DEMO_BABY_ID, record_date, bath_time, bath_note)
        message = "Add bath result: {}".format(result)

    if intent == ADD_MEDICATION:
        record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(MED_DATE) == "today" else getSlotVal(MED_DATE)
        med_time = getSlotVal(MED_TIME)
        med_time = datetime.strptime(record_date + " " + med_time, "%Y-%m-%d %H:%M").isoformat()
        med_note = getSlotVal(MED_NOTE)

        # if user invoke the "add medication" intent, they should offer a medication type. should not be None
        med_type = getSlotVal(MED_TYPE)
        result = add_medicine(DEMO_BABY_ID, record_date, med_time, med_type, med_note)
        message = "Add medicine result: {}".format(result)

    if intent == GET_RECORD:
        record_type = getSlotVal(RECORD_TYPE)
        # if intent == "getMostRecentHeight":  # for query: "What is her last-taken height?"
        if record_type == "last_height":
            result = get_most_recent_height(DEMO_BABY_ID)
            message = "Most recent height was {} inches on {}".format(result[0], result[1])

        # if intent == "getMostRecentWeight":  # for query: "What is her last-taken weight?"
        if record_type == "last_weight":
            result = get_most_recent_weight(DEMO_BABY_ID)
            message = "Most recent weight was {} pounds on {}".format(result[0], result[1])

        # if intent == "getMostRecentHeadCircumference":  # for query: "What is her last-taken head circumference?"
        if record_type == "last_head":
            result = get_most_recent_head_circumference(DEMO_BABY_ID)
            message = "Most recent head circumference was {} inches on {}".format(result[0], result[1])

        # if intent == "getMostRecentVaccineDay":  # for query: "What is her last-taken vaccine?"
        if record_type == "last_vaccine":
            result = get_most_recent_vaccine(DEMO_BABY_ID)
            message = "Most recent vaccine taken was {} on {}".format(result[0], result[1])

        # if intent == "getMostRecentSleepStart":  # for query: "When did she fall asleep?"
        if record_type == "last_sleep_start":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(RECORD_DATE)
            # record_date = getSlotVal(RECORD_DATE)
            result = get_most_recent_sleep_start(DEMO_BABY_ID, record_date)
            message = "Fell asleep at {}".format(result)

        # if intent == "getMostRecentSleepEnd":  # for query: "When did she last wake up?"
        if record_type == "last_sleep_end":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_most_recent_sleep_end(DEMO_BABY_ID, record_date)
            message = "Last woke up at {}".format(result)

        # if intent == "getMostRecentSleepDuration":  # for query: "How long was her last sleep?"
        if record_type == "sleep_duration":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_most_recent_sleep_duration(DEMO_BABY_ID, record_date)
            # result = format_timedelta(duration)
            message = "Last slept for {}".format(result)

        # if intent == "getTotalSleepTime":  # for query: "How long did she sleep in total today?"
        if record_type == "total_sleep":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            duration = get_total_sleep_time(DEMO_BABY_ID, record_date)
            result = format_timedelta(duration)
            message = "Slept for {} in total".format(result)

        # if intent == "getTotalSleepCount":  # for query: "How many times has she slept today?"
        if record_type == "sleep_count":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_total_sleep_count(DEMO_BABY_ID, record_date)
            message = "Slept for {} time(s)".format(result)

        # if intent == "getMostRecentBottleFeed":  # for query: "How much formula did she drink last time?"
        if record_type == "last_formula":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_most_recent_bottle_feed(DEMO_BABY_ID, record_date)
            message = "It was {} milliliters at {}".format(result[0], result[1])

        # if intent == "getTotalBottleFeedVolume":  # for query: "How much formula has she had today?"
        if record_type == "formula_vol":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_total_bottle_feed_volume(DEMO_BABY_ID, record_date)
            message = "{} ounces in total".format(result)

        # if intent == "getTotalBottleFeedCount":  # for query: "How many times has she had formula today?"
        if record_type == "formula_count":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_total_bottle_feed_count(DEMO_BABY_ID, record_date)
            message = "{} time(s)".format(result)

        # if intent == "getMostRecentNurseFeedEnd":  # for query: "When was her last nurse fed?"
        if record_type == "last_nurse":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_most_recent_nurse_feed_end(DEMO_BABY_ID, record_date)
            message = "Last nurse fed at {}".format(result)

        # if intent == "getTotalNurseFeedCount":  # for query: "How many times has she been nurse fed today?"
        if record_type == "nurse_count":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_total_nurse_feed_count(DEMO_BABY_ID, record_date)
            message = "Nurse fed {} time(s)".format(result)

        # if intent == "getMostRecentSolidFood":  # for query: "What was the most recent solid food she had?"
        if record_type == "last_solid":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_most_recent_solid_food(DEMO_BABY_ID, record_date)
            message = "Most recent solid food was {} at {}".format(result[0], result[1])

        # if intent == "getTotalSolidFoodCount":  # for query: "How many times has she had solid food today?"
        if record_type == "solid_count":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_total_solid_food_count(DEMO_BABY_ID, record_date)
            message = "Had solid food {} time(s)".format(result)

        # if intent == "getAllSolidFoodTypes":  # for query: "What types of solid foods has she had today?"
        if record_type == "solid_type":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_all_solid_food_types(DEMO_BABY_ID, record_date)
            message = "Solid food types: {}".format(result)

        # if intent == "getMostRecentDiaperPee":  # for query: "When was her last pee-pee?"
        if record_type == "last_pee":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_most_recent_diaper_pee(DEMO_BABY_ID, record_date)
            message = "Last pee-pee at {}".format(result)

        # if intent == "getTotalDiaperPeeCount":  # for query: "How many times has she peed today?"
        if record_type == "pee_count":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_total_diaper_pee_count(DEMO_BABY_ID, record_date)
            message = "Peed {} time(s)".format(result)

        # if intent == "getMostRecentDiaperPoo":  # for query: "When was her last poo-poo?"
        if record_type == "last_poo":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_most_recent_diaper_poo(DEMO_BABY_ID, record_date)
            message = "Last poo-poo at {}".format(result)

        # if intent == "getTotalDiaperPooCount":  # for query: "How many times has she pooped today?"
        if record_type == "poo_count":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_total_diaper_poo_count(DEMO_BABY_ID, record_date)
            message = "Pooped {} time(s)".format(result)

        # if intent == "getMostRecentBath":  # for query: "When did she have a bath?" (Suppose she has bathed in the current day)
        if record_type == "last_bath":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_most_recent_bath(DEMO_BABY_ID, record_date)
            message = "Last bathed at {}".format(result)

        # if intent == "getMostRecentMedicine":  # for query: "What was the last medication she took?"
        if record_type == "last_med":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_most_recent_medicine(DEMO_BABY_ID, record_date)
            message = "Last took {} at {}".format(result[0], result[1])

        # if intent == "getTotalMedicineCount":  # for query: "How many times has she taken medication today?"
        if record_type == "med_count":
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                RECORD_DATE)
            result = get_total_medicine_count(DEMO_BABY_ID, record_date)
            message = "Had medicine {} time(s)".format(result)

    if intent == DELETE_RECORD:
        delete_type = getSlotVal(DELETE_TYPE)
        if delete_type == "last_sleep": # "Delete her last sleep record"
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d') if getSlotVal(RECORD_DATE) == "today" else getSlotVal(
                    RECORD_DATE)
            result = delete_most_recent_sleep_record(DEMO_BABY_ID, record_date)
            message = "Delete most recent sleep record result: {}".format(result)

    if intent == UPDATE_RECORD:
        update_type = getSlotVal(UPDATE_TYPE)

        if update_type == "last_vaccine_date":    # "Update her last vaccine date to yesterday"
            vaccine_date = getSlotVal(UPDATE_DATE)
            result = update_most_recent_vaccine_date(DEMO_BABY_ID, vaccine_date)
            message = "Update most recent vaccine date result: {}".format(result)

        if update_type == "last_sleep":   # "update start/end time of last sleep to now"
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d')
            sleep_time = getSlotVal(UPDATE_TIME)
            sleep_time = datetime.strptime(record_date + " " + sleep_time, "%Y-%m-%d %H:%M").isoformat()
            start_end = getSlotVal(START_END)
            start_time = sleep_time if start_end == "start" else None
            end_time = sleep_time if start_end == "finish" else None
            result = update_most_recent_sleep_record(DEMO_BABY_ID, record_date, start_time, end_time)
            message = "Update most recent sleep record result: {}".format(result)

        if update_type == "last_formula_vol":   # "Update her last bottle fed volume to 40 ml"
            record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d')
            formula_volume = getSlotVal(UPDATE_DATA)
            result = update_most_recent_bottle_feed(DEMO_BABY_ID, record_date, formula_volume)
            message = "Update most recent bottle feed result: {}".format(result)

    if intent == ENABLE_PREMIUM_FEATURE:  # e.g, user says "lex, enable my premium feature access"
        # bucket name comes from predefined constant value, only input should be user id, e.g, DEMO_BABY_ID

        # first check if bucket exists, if not, create it
        s3_resource = boto3.resource('s3')
        exists = s3_resource.Bucket(USER_ASSET_S3_BUCKET_NAME) in s3_resource.buckets.all()

        # create S3 boto3 client
        s3 = boto3.client('s3')
        if not exists:
            s3.create_bucket(Bucket=USER_ASSET_S3_BUCKET_NAME)

        # create sub-folder inside the bucket based on user id
        s3.put_object(Bucket=USER_ASSET_S3_BUCKET_NAME, Key=(DEMO_BABY_ID + '/'))

        message = "Sure. Successfully enabled the premium feature."

    if intent == CONSULT_AI:
        user_utterance = getSlotVal(CONSULT)
        message = get_openai_response(DEMO_BABY_ID, user_utterance)

    actionType = ""
    if intent == GET_RECORD or intent == DELETE_RECORD or intent == UPDATE_RECORD or intent == ENABLE_PREMIUM_FEATURE or intent == CONSULT_AI:
        actionType = "Close"
    else:
        actionType = "Delegate"


    # Generate response
    response = {
        "sessionState": {
            "dialogAction": {
                "type": actionType
            },
            "intent": {
                "name": intent,
                "slots": slots,
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
                # "content": "YAY, connected!"
            }
        ]
    }

    return response


def delegate(intent: str, slots: any):
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Delegate"  # let the bot decide what to do next
            },
            "intent": {
                "name": intent,
                "slots": slots
            }
        }
    }


def text_to_speech(message):
    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    session = Session(profile_name="adminuser")
    polly = session.client("polly")

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=message, OutputFormat="mp3",
                                            VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
               output = os.path.join(gettempdir(), "speech.mp3")

               try:
                # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                       file.write(stream.read())
               except IOError as error:
                  # Could not write to file, exit gracefully
                  print(error)
                  sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)
    # p
    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])


def main(event, context):
    print('request: {}'.format(json.dumps(event)))

    intent = event["sessionState"]["intent"]["name"]
    slots = event["sessionState"]["intent"]["slots"]

    # print(event["invocationSource"])
    # print(intent)
    # print(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        response = delegate(intent, slots)

    if event["invocationSource"] == "FulfillmentCodeHook":
        response = dispatch(intent, slots)

    # response = dispatch(intent, slots)
    # message = response["messages"][0]["content"]
    # text_to_speech(message)

    return response

