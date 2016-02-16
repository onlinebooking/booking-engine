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
    Get step timedelta: The smaller duration of service_recipe's periods
    """
    def diff(start, end):
        return end - start
    res_delta_diffs = compose(map(lambda p: diff(*p)), get('delta_periods'))
    return compose(min, map(min), map(res_delta_diffs))(service_recipe)


def get_resource_occupation(candidate_resources, dt_range, new_occupations):
    """
    """
    for resource in candidate_resources:
        resource_new_occupations = [y[1] for y in filter(lambda x: x[0] == resource, new_occupations)]

        # Check availability
        availability = resource.get('availability')
        if availability and not is_datetime_range_available(dt_range, availability):
            continue

        # Check occupations
        occupations = resource.get('occupation', []) + resource_new_occupations
        overlappings = [overlaps(dt_range, o) for o in occupations]
        if any(overlappings):
            continue

        return resource

    return None


def get_resources_for_dt_range(loop_dt_range, service_recipe, resources):
    """

    """
    new_occupations = []

    for resource_needed in service_recipe:
        candidate_resources = filter(
            lambda r: r['type'] == resource_needed['type'],
            resources)

        for period in resource_needed['delta_periods']:
            dt_range = by_timedelta_range(period, loop_dt_range[0])

            new_occupations_for_type = filter(
                lambda r: r[0]['type'] == resource_needed['type'],
                new_occupations)
            available_resource = get_resource_occupation(
                candidate_resources, dt_range, new_occupations_for_type)

            if available_resource is None:
                return None

            clean_resource = omit(available_resource,
                                  'occupations', 'availability')
            new_occupations.append((clean_resource, dt_range))

        # per ogni delta_period in resource_needed
        #    - creo relativo dt_range
        #    - per ogni risorsa disponibilie
        #       - controllo availability per dt_range
        #       - controllo occupation per dt_range

    return new_occupations


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

        resources_for_dt_range = get_resources_for_dt_range(loop_dt_range,
                                                            service_recipe,
                                                            resources)
        if resources_for_dt_range:
            ranges.append((loop_dt_range, resources_for_dt_range))

        # like i++ but more cool
        loop_dt_range = by_timedelta_range(
            (delta_step, delta_step + delta_duration), loop_dt_range[0])

    return ranges
