from datetime import datetime, timedelta
from toolz import compose

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def format_date(d):
    return d.strftime('%Y-%m-%d')

def date_with_year(year, d):
    if (d.month == 2 and d.day == 29 and year % 4 != 0):
        return None
    else:
        return d.replace(year=year)

def start_of_day(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def tomorrow(d):
    return d + timedelta(days=1)

def yesterday(d):
    return d - timedelta(days=1)

def start_of_tomorrow(dt):
    return compose(tomorrow, start_of_day)(dt)

def start_of_yesterday(dt):
    return compose(yesterday, start_of_day)(dt)
