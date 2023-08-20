

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
