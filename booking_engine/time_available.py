from toolz import partial, merge, flip
from datetime import time, datetime
from util.funct import any_match, first_match
from util.time import date_with_year, yesterday, tomorrow
from datetime_range import (
    by_time_range, contains, is_same_date, end_after_or_eq, merge_ranges,
)


def defaulitize_availability(availability={}):
    """
    Set defualts to availability, return new object with defaults.
    """
    default_availability = {
        'fixed_closing_days': [],
        'special_closing_days': [],
        'week_working_hours': {},
        'special_working_hours': {},
    }
    return merge(default_availability, availability)


def is_date_a_fixed_closing_date(d, fixed_closing_days=[]):
    """
    Check if date is in given list of dates, does not look at year to
    compare.
    """
    return d in filter(None, map(partial(date_with_year, d.year),
                                 fixed_closing_days))


def is_date_a_special_closing_date(d, special_closing_days=[]):
    """
    Check if date is in given list of dates.
    """
    return d in special_closing_days


def is_date_a_week_working_date(d, week_working_hours={}):
    """
    Check if date is in given dict of working hours mapped by weekday.
    """
    return d.weekday() in week_working_hours


def is_date_a_special_working_date(d, special_working_hours={}):
    """
    Check if date is in given dict of working hours mapped by date.
    """
    return d in special_working_hours


def is_date_available(d, availability={}):
    """
    Checks if date is availabile in given availability.
    """
    a = defaulitize_availability(availability)

    if is_date_a_special_closing_date(d, a['special_closing_days']):
        return False

    if is_date_a_special_working_date(d, a['special_working_hours']):
        return True

    if is_date_a_fixed_closing_date(d, a['fixed_closing_days']):
        return False

    return is_date_a_week_working_date(d, a['week_working_hours'])


def working_hours_of_date(d, special_working_hours={}, week_working_hours={}):
    """
    Working hours of date.
    """
    if is_date_a_special_working_date(d, special_working_hours):
        return special_working_hours[d]
    elif is_date_a_week_working_date(d, week_working_hours):
        return week_working_hours[d.weekday()]

    return []


def working_hours_to_datetime_ranges(d, working_hours):
    """
    Convert working_hours to datetime_ranges on specific date.
    """
    partial_by_time_range = partial(flip(by_time_range), d)
    return map(partial_by_time_range, working_hours)


def are_working_hours_contiguous(working_hours_start, working_hours_end):
    """
    Check if two working_hours are contiguous.
    """
    if not len(working_hours_start) or not len(working_hours_end):
        return False

    return (working_hours_start[-1][1] == time(0) and
            working_hours_end[0][0] == time(0))


def working_datetime_ranges_of_date(d,
                                    special_working_hours={},
                                    week_working_hours={},
                                    merge_tomorrow=True):
    """
    Returns a list of datetimes tuples (datetime_range),
    indicating contiguous working periods of given date, if merge_tomorrow
    check if first period of tomorrow is contiguous and merge
    with last of today.
    """

    # curried on working hours
    whs_by_date = partial(working_hours_of_date,
                          special_working_hours=special_working_hours,
                          week_working_hours=week_working_hours)
    # curried on date
    whs_to_dt_ranges = partial(working_hours_to_datetime_ranges, d)

    today_working_hours = whs_by_date(d)

    if not len(today_working_hours):
        return []

    if not merge_tomorrow:
        return whs_to_dt_ranges(today_working_hours)

    tomorrow_working_hours = whs_by_date(tomorrow(d))

    if are_working_hours_contiguous(today_working_hours,
                                    tomorrow_working_hours):
        # last range of today become a merged range between
        # the last of today and the first of tomorrow

        next_day = tomorrow(d)

        # when tomorrow working hour end at 00:00, certainly is (00:00, 00:00)
        # because is a contiguous with today working hours, in this case
        # we add a day to current date because end at 00:00 of day after
        # this cover 24/7 like situation
        if tomorrow_working_hours[0][1] == time(0):
            next_day = tomorrow(next_day)

        last_period = (
            datetime.combine(d, today_working_hours[-1][0]),
            datetime.combine(next_day, tomorrow_working_hours[0][1])
        )

        return whs_to_dt_ranges(today_working_hours[:-1]) + [last_period]

    return whs_to_dt_ranges(today_working_hours)


def is_datetime_range_available(dt_range, availability={}):
    """
    Checks if a datetime_range is compatible with availability.
    """
    a = defaulitize_availability(availability)
    start_date, end_date = dt_range[0].date(), dt_range[1].date()

    # check if working_hours of date by current availability
    # contains current datetime_range
    def contains_dt_range_in_wh_of_date(d, merge_tomorrow=True):
        working_dt_ranges = working_datetime_ranges_of_date(
            d, a['special_working_hours'], a['week_working_hours'],
            merge_tomorrow=merge_tomorrow)
        return any_match(partial(flip(contains), dt_range), working_dt_ranges)

    if (is_date_available(start_date, a) and
            contains_dt_range_in_wh_of_date(
                start_date,
                merge_tomorrow=is_date_available(tomorrow(start_date), a))):
        return True

    if is_same_date(dt_range):
        return (is_date_available(yesterday(start_date), a) and
                contains_dt_range_in_wh_of_date(yesterday(start_date),
                                                merge_tomorrow=False))

    return False


def nearest_working_datetime_range(dt_range, availability={}):
    """
    Nearest working datetime_range by datetime_range.
    """
    a = defaulitize_availability(availability)
    start_date = dt_range[0].date()

    if not is_date_available(start_date, a):
        return None

    tomorrow_available = is_date_available(tomorrow(start_date), a)
    working_dt_ranges = working_datetime_ranges_of_date(
        start_date,
        a['special_working_hours'], a['week_working_hours'],
        merge_tomorrow=tomorrow_available)

    is_near = partial(flip(end_after_or_eq), dt_range)
    return first_match(is_near, working_dt_ranges)
