from datetime import datetime, time
from time_util import tomorrow

# create a new datetime_range by a timedelta_range and datetime object
def by_timedelta_range(timedelta_range, dt):
    start_timedelta, end_timedelta = timedelta_range
    return dt + start_timedelta, dt + end_timedelta

# create a new datetime_range by a time_range and date object
def by_time_range(time_range, d, span_tomorrow=False):
    start_time, end_time = time_range

    if span_tomorrow or end_time <  start_time:
        return datetime.combine(d, start_time), datetime.combine(tomorrow(d), end_time)
    else:
        return datetime.combine(d, start_time), datetime.combine(d, end_time)

# check if a datetime_range start and end in the same date
def is_same_date(dt_range):
    start_dt, end_dt = dt_range
    return start_dt.date() == end_dt.date()

# check if two given datetime_ranges equals
def equals(dt_range_1, dt_range_2):
    start_dt_1, end_dt_1 = dt_range_1
    start_dt_2, end_dt_2 = dt_range_2

    return start_dt_1 == start_dt_2 and end_dt_1 == end_dt_2

# check if a datetime_range overlaps another datetime_range
def overlaps(dt_range, overlapped_dt_range):
    start_dt, end_dt = dt_range
    over_start_dt, over_end_dt = overlapped_dt_range

    return start_dt < over_end_dt and end_dt > over_start_dt

# cehck if a datetime_range contains another datetime_range
def contains(dt_range, contained_dt_range):
    start_dt, end_dt = dt_range
    cont_start_dt, cont_end_dt = contained_dt_range

    return start_dt <= cont_start_dt and end_dt >= cont_end_dt

# check if a datetime_range end after or equalt to another datetime_range
def end_after_or_eq(dt_range_1, dt_range_2):
    start_dt_1, end_dt_1 = dt_range_1
    start_dt_2, end_dt_2 = dt_range_2

    return end_dt_1 >= end_dt_2

# yes, in a perfect world do end_after, end_before and end_before_or_eq


def merge_dts(dt1, dt2):
    return dt1[0], dt2[1]
    

