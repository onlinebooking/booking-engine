from datetime import datetime, time
from time_util import tomorrow


def by_timedelta_range(timedelta_range, dt):
    """
    Create a new datetime_range by a timedelta_range and datetime object.
    """
    return dt + timedelta_range[0], dt + timedelta_range[1]


def by_time_range(time_range, d, span_tomorrow=False):
    """
    Create a new datetime_range by a time_range and date object.
    """
    start_time, end_time = time_range

    if start_time == end_time and not span_tomorrow:
        return None

    if span_tomorrow or end_time < start_time:
        return datetime.combine(d, start_time), datetime.combine(tomorrow(d),
                                                                 end_time)
    else:
        return datetime.combine(d, start_time), datetime.combine(d, end_time)


def is_same_date(dt_range):
    """
    Check if a datetime_range start and end in the same date.
    """
    return dt_range[0].date() == dt_range[1].date()


def overlaps(dt_range, over_dt_range):
    """
    Check overlaps between two given datetime_ranges, extremes are
    excluded from overlapping.
    """
    return dt_range[0] < over_dt_range[1] and dt_range[1] > over_dt_range[0]


def contains(dt_range, cont_dt_range):
    """
    Check if a datetime_range contains another datetime_range, extremes
    are included.
    """
    return dt_range[0] <= cont_dt_range[0] and dt_range[1] >= cont_dt_range[1]


def end_after_or_eq(dt_range_1, dt_range_2):
    """
    Check if a datetime_range end after or equalt to another datetime_range.
    """
    return dt_range_1[1] >= dt_range_2[1]


def merge_ranges(dt_range_1, dt_range_2):
    """
    Merge two ranges: use the start of first and the end of second.
    """
    return dt_range_1[0], dt_range_2[1]
