from toolz import partial, merge, flip
from time_util import parse_date, date_with_year, format_date, yesterday, tomorrow
from datetime_range import by_time_range, contains, is_same_date, end_after_or_eq, merge_ranges
from funct_util import any_match, first_match
from datetime import time

def defaulitize_availability(availability = {}):
    default_availability = {
        'fixed_closing_days': [],
        'special_closing_days': [],
        'week_working_hours': {},
        'special_working_hours': {},
    }
    return merge(default_availability, availability)

def is_date_a_fixed_closing_date(d, fixed_closing_days = []):
    return d in filter(None, map(partial(date_with_year, d.year), fixed_closing_days))

def is_date_a_special_closing_date(d, special_closing_days = []):
    return d in special_closing_days

def is_date_a_week_working_date(d, week_working_hours = {}):
    return d.weekday() in week_working_hours

def is_date_a_special_working_date(d, special_working_hours = {}):
    return d in special_working_hours

def is_date_available(d, availability = {}):
    a = defaulitize_availability(availability)

    if is_date_a_special_closing_date(d, a['special_closing_days']):
        return False

    if is_date_a_special_working_date(d, a['special_working_hours']):
        return True

    if is_date_a_fixed_closing_date(d, a['fixed_closing_days']):
        return False

    return is_date_a_week_working_date(d, a['week_working_hours'])


def concrete_working_hours(d, special_working_hours = {}, week_working_hours = {}):
    """
    """
    if is_date_a_special_working_date(d, special_working_hours):
        return special_working_hours[d]
    elif is_date_a_week_working_date(d, week_working_hours):
        return week_working_hours[d.weekday()]
    
    return []



# @memorized????????
def working_hours_of_date(d, special_working_hours = {}, week_working_hours = {}, merge=True):
    """
    Returns a list of datetimes tuples (datetime_range),
    indicating contiguous working periods.

    """

    def to_dt_ranges(wh, span_tomorrow=False):
        by_time_range_span_tomorrow = partial(by_time_range, span_tomorrow=span_tomorrow)
        partial_by_time_range = partial(flip(by_time_range_span_tomorrow), d)
        return filter(None, map(partial_by_time_range, wh))

    
    today_working_hours = concrete_working_hours(d, special_working_hours, week_working_hours)
    if not merge:
        return to_dt_ranges(today_working_hours)
    
    tomorrow_working_hours = concrete_working_hours(tomorrow(d), special_working_hours, week_working_hours)

    if not len(today_working_hours):
        return []

    if len(tomorrow_working_hours):
        if today_working_hours[-1][1] == time(0) and tomorrow_working_hours[0][0] == time(0):
            today_working_hours[-1] = merge_ranges(today_working_hours[-1], tomorrow_working_hours[0])
            return to_dt_ranges(today_working_hours[:-1]) + to_dt_ranges([today_working_hours[-1]], True) 
            
    return to_dt_ranges(today_working_hours)  

    

def is_datetime_range_available(dt_range, availability = {}):
    """
    Checks if a datetime_range is compatible with availability.
    """
    a = defaulitize_availability(availability)

    start_dt, end_dt = dt_range
    start_date, end_date = start_dt.date(), end_dt.date()

    # check if working_hours of date by current availability
    # contains current datetime_range
    def contains_in_wh_of_date(d, merge=True):
        working_hours = working_hours_of_date(d, 
            a['special_working_hours'], a['week_working_hours'], merge=merge)
        return any_match(partial(flip(contains), dt_range), working_hours)

    
    tomorrow_available = is_date_available(tomorrow(start_date), a)
    if is_date_available(start_date, a) and contains_in_wh_of_date(start_date, merge=tomorrow_available):
        return True

    if is_same_date(dt_range):
        return is_date_available(yesterday(start_date), a) and contains_in_wh_of_date(yesterday(start_date), merge=False)    
    
    return False


def nearest_working_datetime_range(dt_range, availability = {}):
    """
    nearest working datetime_range by datetime_range
    """
    a = defaulitize_availability(availability)
    start_dt, end_dt = dt_range

    tomorrow_available = is_date_available(tomorrow(start_dt.date()), a)
    working_hours = working_hours_of_date(start_dt.date(), a['special_working_hours'], 
        a['week_working_hours'], merge=tomorrow_available)
    
    return first_match(partial(flip(end_after_or_eq), dt_range), working_hours)
