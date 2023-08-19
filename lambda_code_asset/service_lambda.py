import json
from datetime import datetime

from busy_baby.api import create_baby, add_growth_record, add_vaccine_record, add_bottle_feed, add_sleep_record, \
    add_nurse_feed, add_solid_food, add_diaper_pee, add_diaper_poo, add_bath, add_medicine
from busy_baby.constants import DEMO_BABY_ID, FIRST_NAME, LAST_NAME, GENDER, BIRTHDAY, ADD_BABY, ADD_GROWTH, \
    ADD_VACCINE, ADD_SLEEP, ADD_FORMULA, ADD_NURSING, ADD_FOOD, ADD_BATH, ADD_MEDICATION, DELIVERY_TIME, GROWTH_DATE, \
    GROWTH_TYPE, GROWTH_DATA, VACCINE_DATE, VACCINE_TYPE, SLEEP_TIME, START_END, FORMULA_TIME, FORMULA_VOLUME, \
    NURSING_TIME, FOOD_TIME, FOOD_TYPE, ADD_DIAPER, DIAPER_TYPE, DIAPER_TIME, BATH_TIME, MED_TIME, MED_TYPE, SLEEP_DATE, \
    FORMULA_DATE, NURSING_DATE, FOOD_DATE, DIAPER_DATE, BATH_DATE, MED_DATE, MED_NOTE, BATH_NOTE, DIAPER_NOTE, \
    FOOD_NOTE, NURSING_NOTE, FORMULA_NOTE, SLEEP_NOTE, VACCINE_NOTE


def dispatch(intent: str, slots: any):
    def getSlotVal(slotName):
        return slots[slotName]["value"]["interpretedValue"]

    response = {}
    message = ''

    # dispatch to different service based on different intent

    if intent == ADD_BABY:
        # first_name = slots[FIRST_NAME]["value"]["interpretedValue"]
        # last_name = slots[LAST_NAME]["value"]["interpretedValue"]
        # gender = slots[GENDER]["value"]["interpretedValue"]
        # birthday = slots[BIRTHDAY]["value"]["interpretedValue"]
        # delivery_time = slots[DELIVERY_TIME]["value"]["interpretedValue"]
        first_name = getSlotVal(FIRST_NAME)
        last_name = getSlotVal(LAST_NAME)
        gender = getSlotVal(GENDER)
        birthday = getSlotVal(BIRTHDAY)
        delivery_time = getSlotVal(DELIVERY_TIME)

        result = create_baby(first_name, last_name, gender, birthday, delivery_time)
        message = "Baby profile creation result: {}".format(result)

    if intent == ADD_GROWTH:
        record_date = slots[GROWTH_DATE]["value"]["interpretedValue"]
        # if record_date == "today":
        #     record_date = datetime.utcnow().strftime('%Y-%m-%d')  # convert current UTC date to strings
        #
        # if "Height" in slots and "value" in slots["Height"]:
        #     height = slots["Height"]["value"]["interpretedValue"]
        # else:
        #     height = None  # because height is optional field, hence can be None if not provided by upstream (e.g, Lex)
        #
        # if "Weight" in slots and "value" in slots["Weight"]:
        #     weight = slots["Weight"]["value"]["interpretedValue"]
        # else:
        #     weight = None
        #
        # if "HeadCircumference" in slots and "value" in slots["HeadCircumference"]:
        #     head_circumference = slots["HeadCircumference"]["value"]["interpretedValue"]
        # else:
        #     head_circumference = None

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
        # if "StartTime" in slots and "value" in slots["StartTime"]:
        #     start_time = slots["StartTime"]["value"]["interpretedValue"]
        # else:
        #     start_time = None
        #
        # if "EndTime" in slots and "value" in slots["EndTime"]:
        #     end_time = slots["EndTime"]["value"]["interpretedValue"]
        # else:
        #     end_time = None

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
        # if formula_time == "now":
        #     formula_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        formula_volume = getSlotVal(FORMULA_VOLUME)
        formula_note = getSlotVal(FORMULA_NOTE)
        result = add_bottle_feed(DEMO_BABY_ID, record_date, formula_time, formula_volume, formula_note)
        message = "Add bottle feed result: {}".format(result)

    if intent == ADD_NURSING:
        record_date = datetime.utcnow().strftime('%Y-%m-%d') if getSlotVal(NURSING_DATE) == "today" else getSlotVal(NURSING_DATE)
        # if "StartTime" in slots and "value" in slots["StartTime"]:
        #     start_time = slots["StartTime"]["value"]["interpretedValue"]
        # else:
        #     start_time = None
        #
        # if "EndTime" in slots and "value" in slots["EndTime"]:
        #     end_time = slots["EndTime"]["value"]["interpretedValue"]
        # else:
        #     end_time = None

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

    # # if intent == "addDiaperPee":
    #     record_date = datetime.utcnow().strftime('%Y-%m-%d')
    #     diaper_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') if getSlotVal(DIAPER_TIME)=="now" else getSlotVal(DIAPER_TIME)
    #     result = add_diaper_pee(DEMO_BABY_ID, record_date, diaper_time)
    #     message = "Add diaper pee result: {}".format(result)
    #
    # if intent == "addDiaperPoo":
    #     record_date = datetime.utcnow().strftime('%Y-%m-%d')
    #     diaper_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') if getSlotVal(DIAPER_TIME)=="now" else getSlotVal(DIAPER_TIME)
    #     result = add_diaper_poo(DEMO_BABY_ID, record_date, diaper_time)
    #     message = "Add diaper poo result: {}".format(result)

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

        # med_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') if getSlotVal(MED_TIME) == "now" else getSlotVal(MED_TIME)
        # if "MedType" in slots and "value" in slots["MedType"]:
        #     med_type = slots["MedType"]["value"]["interpretedValue"]
        # else:
        #     med_type = None

        # if user invoke the "add medication" intent, they should offer a medication type. should not be None
        med_type = getSlotVal(MED_TYPE)
        result = add_medicine(DEMO_BABY_ID, record_date, med_time, med_type, med_note)
        message = "Add medicine result: {}".format(result)

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
    - getMostRecentVaccineDay(baby_id, date)
    - getAllVaccineTypes(baby_id, date)
    - getMostRecentSleepStart(baby_id, date)
    - getMostRecentSleepEnd(baby_id, date)
    - getMostRecentSleepDuration(baby_id, date)
    - getTotalSleepTime(baby_id, date)
    - getTotalSleepCount(baby_id, date)
    - getMostRecentBottleFeedTime(baby_id, date)
    - getMostRecentBottleFeedVolume(baby_id, date)
    - getTotalBottleFeedVolume(baby_id, date)
    - getTotalBottleFeedCount(baby_id, date)
    - getMostRecentNurseFeedEnd(baby_id, date)
    - getTotalNurseFeedCount(baby_id, date)
    - getMostRecentSolidFoodTime(baby_id, date)
    - getMostRecentSolidFoodType(baby_id, date)
    - getTotalSolidFoodCount(baby_id, date)
    - getAllSolidFoodTypes(baby_id, date)
    - getMostRecentDiaperPeeTime(baby_id, date)
    - getTotalDiaperPeeCount(baby_id, date)
    - getMostRecentDiaperPooTime(baby_id, date)
    - getTotalDiaperPooCount(baby_id, date)
    - getMostRecentBathTime(baby_id, date)
    - getMostRecentMedicineTime(baby_id, date)
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

