from pytz import timezone
from datetime import datetime

tz = timezone('EST')

def get_time():
    return datetime.now(tz)

def get_time_formatted():
    now = datetime.now(tz)
    now = now.strftime("%m/%d/%Y, %H:%M")
    return now