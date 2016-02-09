from datetime import date, time, datetime, timedelta
from toolz import compose


def parse_date(date_str):
    """
    Parse date using Y-m-d format.
    """
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def format_date(d):
    """
    Format date in Y-m-d.
    """
    return d.strftime('%Y-%m-%d')


def date_with_year(year, d):
    """
    Set year to a date object, given None when the date is 29 Feb
    and year is not a leap year.
    """
    if (d.month == 2 and d.day == 29 and year % 4 != 0):
        return None
    else:
        return d.replace(year=year)


def start_of_day(d):
    """
    The start of day 00:00:00 of given datetime/date object.
    """
    start_time = time(hour=0, minute=0, second=0, microsecond=0)
    only_date = d.date() if isinstance(d, datetime) else d
    return datetime.combine(only_date, start_time)


def tomorrow(d):
    """
    Tomorrow of given datetime/date.
    """
    return d + timedelta(days=1)


def yesterday(d):
    """
    Yesterday of given datetime/date.
    """
    return d - timedelta(days=1)


def start_of_tomorrow(d):
    """
    Tomrrow start of day of given datetime/date.
    """
    return compose(tomorrow, start_of_day)(d)


def start_of_yesterday(d):
    """
    Yesterday start of day of given datetime/date.
    """
    return compose(yesterday, start_of_day)(d)
