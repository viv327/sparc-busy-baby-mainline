
from .models.daily_record import DailyRecord
# from .api import get_total_sleep_time, get_total_bottle_feed_volume
from datetime import datetime, timedelta
import dateutil.tz


def format_timedelta(duration):
    # helper function to format datetime.timedelta format time duration into user readable string
    # seconds are ignored
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    formatted_duration = ""

    if duration.days > 0:
        formatted_duration += f"{duration.days} day{'s' if duration.days != 1 else ''} "

    if hours > 0:
        formatted_duration += f"{hours} hour{'s' if hours != 1 else ''} "

    if minutes > 0:
        formatted_duration += f"{minutes} minute{'s' if minutes != 1 else ''}"

    return formatted_duration


# def calculate_daily_sleep_time(baby_id):
#     """
#     e.g, from today, get last 3 days, for each day, call get_total_sleep_time, then finally calculate the result and return
#     """
#     # timeZone = dateutil.tz.gettz('US/Eastern')
#     # record_date = datetime.now(tz=timeZone).strftime('%Y-%m-%d')
#     total_sleep_time = timedelta()
#     today = datetime.today()
#     today_format = today.strftime('%Y-%m-%d')
#     total_sleep_time += get_total_sleep_time(baby_id, today_format)
#     for i in range(2):
#         day = today - timedelta(days=i)
#         day_format = day.strftime('%Y-%m-%d')
#         total_sleep_time += get_total_sleep_time(baby_id, day_format)
#     result = format_timedelta(total_sleep_time)
#     return result
#
#
# def calculate_daily_milk_volume(baby_id):
#     """
#     e.g, from today, get last 3 days, for each day, call get_total_bottle_feed_volume, then finally calculate the result and return
#     """
#     total_bottle_volume = 0
#     today = datetime.today()
#     today_format = today.strftime('%Y-%m-%d')
#     total_bottle_volume += int(get_total_bottle_feed_volume(baby_id, today_format))
#     for i in range(2):
#         day = today - timedelta(days=i)
#         day_format = day.strftime('%Y-%m-%d')
#         total_bottle_volume += int(get_total_bottle_feed_volume(baby_id, day_format))
#     return str(total_bottle_volume)
