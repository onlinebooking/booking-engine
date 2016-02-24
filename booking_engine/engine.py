from datetime import timedelta
from toolz import compose, last
from toolz.curried import map, get
from util.time import start_of_tomorrow
from util.data import omit
from datetime_range import by_timedelta_range, contains, overlaps
from time_available import (
    is_datetime_range_available, nearest_working_datetime_range,
)


def get_service_duration(service_recipe):
    """
    Get duration timedelta: The global duration of service_recipe.
    """
    res_delta_ends = compose(last, lambda p: zip(*p), get('delta_periods'))
    return compose(max, map(max), map(res_delta_ends))(service_recipe)


def get_service_step(service_recipe):
    """
    Get step timedelta: The smaller duration of service_recipe's periods.
    """
    def diff(start, end):
        return end - start
    res_delta_diffs = compose(map(lambda p: diff(*p)), get('delta_periods'))
    return compose(min, map(min), map(res_delta_diffs))(service_recipe)


def clean_resource(resource):
    """
    Resource without occupations and availability.
    """
    return omit(resource, 'occupations', 'availability')


def get_resource_available_in_dt_range(candidate_resources, dt_range,
                                       new_resource_occupations):
    """
    Try to find a resource available in dt_range, if no resource finded return
    None.
    """
    for resource in candidate_resources:

        # Only occupations of current resource
        res_new_occupations = [y[1] for y in filter(
            lambda x: x[0] == clean_resource(resource),
            new_resource_occupations)]

        # Check availability
        availability = resource.get('availability')
        if (availability and not is_datetime_range_available(dt_range,
                                                             availability)):
            continue

        # Check occupations
        occupations = resource.get('occupations', []) + res_new_occupations
        overlappings = [overlaps(dt_range, o) for o in occupations]
        if any(overlappings):
            continue

        return resource

    return None


def get_resource_occupations_in_dt_range(dt_range, service_recipe, resources):
    """
    Return a list of resource occupations (res, dt_range) in given dt_range
    return None when no resources can be allocated.
    """
    new_resource_occupations = []

    for resource_needed in service_recipe:
        candidate_resources = filter(
            lambda r: r['type'] == resource_needed['type'],
            resources)

        for period in resource_needed['delta_periods']:
            period_dt_range = by_timedelta_range(period, dt_range[0])

            new_res_occupations_for_type = filter(
                lambda r: r[0]['type'] == resource_needed['type'],
                new_resource_occupations)
            available_resource = get_resource_available_in_dt_range(
                candidate_resources, period_dt_range,
                new_res_occupations_for_type)

            if available_resource is None:
                return None

            new_resource_occupations.append(
                (clean_resource(available_resource), period_dt_range))

    return new_resource_occupations


def calculate_ranges(period, availability, service_recipe, resources):
    """
    Calculates available time ranges and resulting resources configuration,
    given:
    * period: tuple of two datetimes
    * availability: dict describing global shop availability
    * service_recipe: list of needed resources and relative timings
    * resources: availability (from configuration)
      and occupation (from allocated services) of each resource
    """

    ranges = []

    period_start_dt, period_end_dt = period

    delta_duration = get_service_duration(service_recipe)
    delta_step = get_service_step(service_recipe)

    loop_dt_range = by_timedelta_range((timedelta(0), delta_duration),
                                       period_start_dt)

    while contains(period, loop_dt_range):

        if not is_datetime_range_available(loop_dt_range, availability):
            near_working_dt_range = nearest_working_datetime_range(
                loop_dt_range, availability)

            if near_working_dt_range is not None:
                loop_dt_range = by_timedelta_range(
                    (timedelta(0), delta_duration), near_working_dt_range[0])
            else:
                loop_dt_range = by_timedelta_range(
                    (timedelta(0), delta_duration),
                    start_of_tomorrow(loop_dt_range[0]))

            continue

        resource_occupations = get_resource_occupations_in_dt_range(
            loop_dt_range, service_recipe, resources)
        if resource_occupations:
            ranges.append((loop_dt_range, resource_occupations))

        # like i++ but more cool
        loop_dt_range = by_timedelta_range(
            (delta_step, delta_step + delta_duration), loop_dt_range[0])

    return ranges
