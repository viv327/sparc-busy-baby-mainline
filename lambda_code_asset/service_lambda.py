import json
from datetime import datetime

from busy_baby.api import create_baby, add_growth_record, add_vaccine_record, add_bottle_feed, add_sleep_record, \
    add_nurse_feed, add_solid_food, add_diaper_pee, add_diaper_poo, add_bath, add_medicine, get_most_recent_height, \
    get_most_recent_weight, get_most_recent_head_circumference, get_most_recent_vaccine, get_most_recent_sleep_start, \
    get_most_recent_sleep_end, get_most_recent_sleep_duration, get_total_sleep_time, get_total_sleep_count, \
    get_most_recent_bottle_feed, get_total_bottle_feed_volume, get_total_bottle_feed_count, get_most_recent_nurse_feed_end, \
    get_total_nurse_feed_count, get_most_recent_solid_food, get_total_solid_food_count, get_all_solid_food_types, \
    get_most_recent_diaper_pee, get_total_diaper_pee_count, get_most_recent_diaper_poo, get_total_diaper_poo_count, \
    get_most_recent_bath, get_most_recent_medicine, get_total_medicine_count
from busy_baby.constants import DEMO_BABY_ID, FIRST_NAME, LAST_NAME, GENDER, BIRTHDAY, ADD_BABY, ADD_GROWTH, \
    ADD_VACCINE, ADD_SLEEP, ADD_FORMULA, ADD_NURSING, ADD_FOOD, ADD_BATH, ADD_MEDICATION, DELIVERY_TIME, GROWTH_DATE, \
    GROWTH_TYPE, GROWTH_DATA, VACCINE_DATE, VACCINE_TYPE, SLEEP_TIME, START_END, FORMULA_TIME, FORMULA_VOLUME, \
    NURSING_TIME, FOOD_TIME, FOOD_TYPE, ADD_DIAPER, DIAPER_TYPE, DIAPER_TIME, BATH_TIME, MED_TIME, MED_TYPE, SLEEP_DATE, \
    FORMULA_DATE, NURSING_DATE, FOOD_DATE, DIAPER_DATE, BATH_DATE, MED_DATE, MED_NOTE, BATH_NOTE, DIAPER_NOTE, \
    FOOD_NOTE, NURSING_NOTE, FORMULA_NOTE, SLEEP_NOTE, VACCINE_NOTE, GET_RECORD, RECORD_TYPE


def dispatch(intent: str, slots: any):
    def getSlotVal(slotName):
        return slots[slotName]["value"]["interpretedValue"] if slotName in slots else None

    response = {}
    message = ''

    # dispatch to different service based on different intent

    if intent == ADD_BABY:
        first_name = getSlotVal(FIRST_NAME)
        last_name = getSlotVal(LAST_NAME)
        gender = getSlotVal(GENDER)
        birthday = getSlotVal(BIRTHDAY)
        delivery_time = getSlotVal(DELIVERY_TIME)

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
        record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(VACCINE_DATE) == "today" else getSlotVal(VACCINE_DATE) # convert current UTC date to strings

        vaccine_type = getSlotVal(VACCINE_TYPE)
        vaccine_note = getSlotVal(VACCINE_NOTE)
        result = add_vaccine_record(DEMO_BABY_ID, record_date, vaccine_type, vaccine_note)
        message = "Update baby vaccine record result: {}".format(result)

    if intent == ADD_SLEEP:
        record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(SLEEP_DATE) == "today" else getSlotVal(SLEEP_DATE)

        # intent takes a slot "start_end" which lets user decide if the current record is a start or end time point, then enter the time in slot "sleep time"
        # not in to two slots as "start_time"/"end_time"
        sleep_time = getSlotVal(SLEEP_TIME)
        start_end = getSlotVal(START_END)
        sleep_note = getSlotVal(SLEEP_NOTE)

        start_time = sleep_time if start_end == "start" else None
        end_time = sleep_time if start_end == "end" else None

        result = add_sleep_record(DEMO_BABY_ID, record_date, start_time, end_time, sleep_note)
        message = "Add sleep record result: {}".format(result)

    if intent == ADD_FORMULA:
        record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(FORMULA_DATE) == "today" else getSlotVal(FORMULA_DATE)

        # in current bot design, we only manually set value for date, no such operation for time "now".
        # so if else only needed for date, not for time, as in the current design.
        formula_time = getSlotVal(FORMULA_TIME)
        formula_volume = getSlotVal(FORMULA_VOLUME)
        formula_note = getSlotVal(FORMULA_NOTE)
        result = add_bottle_feed(DEMO_BABY_ID, record_date, formula_time, formula_volume, formula_note)
        message = "Add bottle feed result: {}".format(result)

    if intent == ADD_NURSING:
        record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(NURSING_DATE) == "today" else getSlotVal(NURSING_DATE)

        nursing_time = getSlotVal(NURSING_TIME)
        nursing_note = getSlotVal(NURSING_NOTE)
        start_end = getSlotVal(START_END)

        start_time = nursing_time if start_end == "start" else None
        end_time = nursing_time if start_end == "end" else None

        result = add_nurse_feed(DEMO_BABY_ID, record_date, start_time, end_time, nursing_note)
        message = "Add nurse feed result: {}".format(result)

    if intent == ADD_FOOD:
        record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(FOOD_DATE) == "today" else getSlotVal(FOOD_DATE)
        food_time = getSlotVal(FOOD_TIME)
        food_note = getSlotVal(FOOD_NOTE)
        # food_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') if getSlotVal(FOOD_TIME)=="now" else getSlotVal(FOOD_TIME)
        food_type = getSlotVal(FOOD_TYPE)
        result = add_solid_food(DEMO_BABY_ID, record_date, food_time, food_type, food_note)
        message = "Add solid food result: {}".format(result)

    if intent == ADD_DIAPER:
        diaper_type = getSlotVal(DIAPER_TYPE)
        record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(DIAPER_DATE) == "today" else getSlotVal(DIAPER_DATE)
        diaper_time = getSlotVal(DIAPER_TIME)
        diaper_note = getSlotVal(DIAPER_NOTE)
        # diaper_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') if getSlotVal(DIAPER_TIME) == "now" else getSlotVal(DIAPER_TIME)
        result = add_diaper_poo(DEMO_BABY_ID, record_date, diaper_time, diaper_note) if diaper_type == "poo" else add_diaper_pee(DEMO_BABY_ID, record_date, diaper_time, diaper_note)
        message = "Add diaper {} result: {}".format(diaper_type, result)

    if intent == ADD_BATH:
        record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(BATH_DATE) == "today" else getSlotVal(BATH_DATE)
        bath_time = getSlotVal(BATH_TIME)
        bath_note = getSlotVal(BATH_NOTE)
        # bath_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') if getSlotVal(BATH_TIME) == "now" else getSlotVal(BATH_TIME)
        result = add_bath(DEMO_BABY_ID, record_date, bath_time, bath_note)
        message = "Add bath result: {}".format(result)

    if intent == ADD_MEDICATION:
        record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(MED_DATE) == "today" else getSlotVal(MED_DATE)
        med_time = getSlotVal(MED_TIME)
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
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(SLEEP_DATE) == "today" else getSlotVal(SLEEP_DATE)
            result = get_most_recent_sleep_start(DEMO_BABY_ID, record_date)
            message = "Fell asleep at {}".format(result)

        # if intent == "getMostRecentSleepEnd":  # for query: "When did she last wake up?"
        if record_type == "last_sleep_end":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(SLEEP_DATE) == "today" else getSlotVal(
                SLEEP_DATE)
            result = get_most_recent_sleep_end(DEMO_BABY_ID, record_date)
            message = "Last woke up at {}".format(result)

        # if intent == "getMostRecentSleepDuration":  # for query: "How long was her last sleep?"
        if record_type == "sleep_duration":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(SLEEP_DATE) == "today" else getSlotVal(
                SLEEP_DATE)
            result = get_most_recent_sleep_duration(DEMO_BABY_ID, record_date)
            message = "Last slept for {}".format(result)

        # if intent == "getTotalSleepTime":  # for query: "How long did she sleep in total today?"
        if record_type == "total_sleep":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(SLEEP_DATE) == "today" else getSlotVal(
                SLEEP_DATE)
            result = get_total_sleep_time(DEMO_BABY_ID, record_date)
            message = "Slept for {} hours in total".format(result)

        # if intent == "getTotalSleepCount":  # for query: "How many times has she slept today?"
        if record_type == "sleep_count":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(SLEEP_DATE) == "today" else getSlotVal(
                SLEEP_DATE)
            result = get_total_sleep_count(DEMO_BABY_ID, record_date)
            message = "Slept for {} time(s)".format(result)

        # if intent == "getMostRecentBottleFeed":  # for query: "How much formula did she drink last time?"
        if record_type == "last_formula":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(FORMULA_DATE) == "today" else getSlotVal(
                FORMULA_DATE)
            result = get_most_recent_bottle_feed(DEMO_BABY_ID, record_date)
            message = "It was {} milliliters at {}".format(result[0], result[1])

        # if intent == "getTotalBottleFeedVolume":  # for query: "How much formula has she had today?"
        if record_type == "formula_vol":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(FORMULA_DATE) == "today" else getSlotVal(
                FORMULA_DATE)
            result = get_total_bottle_feed_volume(DEMO_BABY_ID, record_date)
            message = "{} ounces in total".format(result)

        # if intent == "getTotalBottleFeedCount":  # for query: "How many times has she had formula today?"
        if record_type == "formula_count":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(FORMULA_DATE) == "today" else getSlotVal(
                FORMULA_DATE)
            result = get_total_bottle_feed_count(DEMO_BABY_ID, record_date)
            message = "{} time(s)".format(result)

        # if intent == "getMostRecentNurseFeedEnd":  # for query: "When was her last nurse fed?"
        if record_type == "last_nurse":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(NURSING_DATE) == "today" else getSlotVal(
                NURSING_DATE)
            result = get_most_recent_nurse_feed_end(DEMO_BABY_ID, record_date)
            message = "Last nurse fed at {}".format(result)

        # if intent == "getTotalNurseFeedCount":  # for query: "How many times has she been nurse fed today?"
        if record_type == "nurse_count":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(NURSING_DATE) == "today" else getSlotVal(
                NURSING_DATE)
            result = get_total_nurse_feed_count(DEMO_BABY_ID, record_date)
            message = "Nurse fed {} time(s)".format(result)

        # if intent == "getMostRecentSolidFood":  # for query: "What was the most recent solid food she had?"
        if record_type == "last_solid":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(FOOD_DATE) == "today" else getSlotVal(
                FOOD_DATE)
            result = get_most_recent_solid_food(DEMO_BABY_ID, record_date)
            message = "Most recent solid food was {} at {}".format(result[0], result[1])

        # if intent == "getTotalSolidFoodCount":  # for query: "How many times has she had solid food today?"
        if record_type == "solid_count":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(FOOD_DATE) == "today" else getSlotVal(
                FOOD_DATE)
            result = get_total_solid_food_count(DEMO_BABY_ID, record_date)
            message = "Had solid food {} time(s)".format(result)

        # if intent == "getAllSolidFoodTypes":  # for query: "What types of solid foods has she had today?"
        if record_type == "solid_type":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(FOOD_DATE) == "today" else getSlotVal(
                FOOD_DATE)
            result = get_all_solid_food_types(DEMO_BABY_ID, record_date)
            message = "Solid food types: {}".format(result)

        # if intent == "getMostRecentDiaperPee":  # for query: "When was her last pee-pee?"
        if record_type == "last_pee":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(DIAPER_DATE) == "today" else getSlotVal(
                DIAPER_DATE)
            result = get_most_recent_diaper_pee(DEMO_BABY_ID, record_date)
            message = "Last pee-pee at {}".format(result)

        # if intent == "getTotalDiaperPeeCount":  # for query: "How many times has she peed today?"
        if record_type == "pee_count":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(DIAPER_DATE) == "today" else getSlotVal(
                DIAPER_DATE)
            result = get_total_diaper_pee_count(DEMO_BABY_ID, record_date)
            message = "Peed {} time(s)".format(result)

        # if intent == "getMostRecentDiaperPoo":  # for query: "When was her last poo-poo?"
        if record_type == "last_poo":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(DIAPER_DATE) == "today" else getSlotVal(
                DIAPER_DATE)
            result = get_most_recent_diaper_poo(DEMO_BABY_ID, record_date)
            message = "Last poo-poo at {}".format(result)

        # if intent == "getTotalDiaperPooCount":  # for query: "How many times has she pooped today?"
        if record_type == "poo_count":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(DIAPER_DATE) == "today" else getSlotVal(
                DIAPER_DATE)
            result = get_total_diaper_poo_count(DEMO_BABY_ID, record_date)
            message = "Pooped {} time(s)".format(result)

        # if intent == "getMostRecentBath":  # for query: "When did she have a bath?" (Suppose she has bathed in the current day)
        if record_type == "last_bath":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(BATH_DATE) == "today" else getSlotVal(
                BATH_DATE)
            result = get_most_recent_bath(DEMO_BABY_ID, record_date)
            message = "Last bathed at {}".format(result)

        # if intent == "getMostRecentMedicine":  # for query: "What was the last medication she took?"
        if record_type == "last_med":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(MED_DATE) == "today" else getSlotVal(
                MED_DATE)
            result = get_most_recent_medicine(DEMO_BABY_ID, record_date)
            message = "Last took {} at {}".format(result[0], result[1])

        # if intent == "getTotalMedicineCount":  # for query: "How many times has she taken medication today?"
        if record_type == "med_count":
            record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(MED_DATE) == "today" else getSlotVal(
                MED_DATE)
            result = get_total_medicine_count(DEMO_BABY_ID, record_date)
            message = "Had medicine {} time(s)".format(result)

    # Generate response
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
                # "type": "Delegate"
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

    '''
    - createBaby(first_name, last_name, gender, birthday)x
    - addGrowthRecord(baby_id, record_date, height, weight, head_circumference)
    - addVaccineRecord(baby_id, record_date, vaccine_type)
    - addSleepRecord(baby_id, date, start_time, end_time)
    - addBottleFeed(baby_id, date, bottle_time, volume)
    - addNurseFeed(baby_id, date, start_time, end_time)
    - addSolidFood(baby_id, date, food_time, food_type)
    - addDiaperPee(baby_id, date, pee_time)
    - addDiaperPoo(baby_id, date, poo_time)
    - addBath(baby_id, date, bath_time)
    - addMedicine(baby_id, date, medicine_time, medicine_type)

    - getMostRecentHeight(baby_id)
    - getMostRecentWeight(baby_id)
    - getMostRecentHeadCircumference(baby_id)
    - getMostRecentVaccine(baby_id)
    - getMostRecentSleepStart(baby_id, date)
    - getMostRecentSleepEnd(baby_id, date)
    - getMostRecentSleepDuration(baby_id, date)
    - getTotalSleepTime(baby_id, date)
    - getTotalSleepCount(baby_id, date)
    - getMostRecentBottleFeed(baby_id, date)
    - getTotalBottleFeedVolume(baby_id, date)
    - getTotalBottleFeedCount(baby_id, date)
    - getMostRecentNurseFeedEnd(baby_id, date)
    - getTotalNurseFeedCount(baby_id, date)
    - getMostRecentSolidFood(baby_id, date)
    - getTotalSolidFoodCount(baby_id, date)
    - getAllSolidFoodTypes(baby_id, date)
    - getMostRecentDiaperPee(baby_id, date)
    - getTotalDiaperPeeCount(baby_id, date)
    - getMostRecentDiaperPoo(baby_id, date)
    - getTotalDiaperPooCount(baby_id, date)
    - getMostRecentBath(baby_id, date)
    - getMostRecentMedicine(baby_id, date)
    - getTotalMedicineCount(baby_id, date)

    - deleteMostRecentSleepRecord(baby_id)
    - updateMostRecentSleepStartRecord(baby_id, start_time)**********
    - updateMostRecentSleepEndRecord(baby_id, end_time)**********
    - updateMostRecentBottleFeed(baby_id, volume, bottle_time)
    - updateMostRecentVaccineDate...


    '''
    # TODO: add more intents here, each with a handling function
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


def main(event, context):
    print('request: {}'.format(json.dumps(event)))

    intent = event["sessionState"]["intent"]["name"]
    slots = event["sessionState"]["intent"]["slots"]

    print(event["invocationSource"])
    print(intent)
    print(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        response = delegate(intent, slots)

    if event["invocationSource"] == "FulfillmentCodeHook":
        response = dispatch(intent, slots)

    return response

