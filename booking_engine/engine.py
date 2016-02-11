from datetime import timedelta, datetime, date, time
from datetime_range import by_timedelta_range, contains, overlaps
from time_available import ( is_datetime_range_available, 
        nearest_working_datetime_range, working_hours_of_date )
from time_util import start_of_tomorrow
from toolz.dicttoolz import dissoc

# def resources_timedelta(resources):
    # res_ends = compose(last, lambda p: zip(*p), get('periods'))
    # return compose(max, map(max), map(res_ends))(resources)

# def resources_padding_timedelta(resources):
    # diff = lambda start, end: end - start
    # res_diffs = compose(map(lambda p: diff(*p)), get('periods'))
    # return compose(min, map(min), map(res_diffs))(resources)


def get_service_duration(service_recipe):
    """
    """
    #TODO: implement
    # durata totale intervento calcolata
    return timedelta(hours=1)

def get_service_step(service_recipe):
    """
    """
    #TODO: implement
    # step calcolata che sarebbe la minima durata della composizione di risorse
    return timedelta(minutes=30)


def get_resource_occupation(candidate_resources, dt_range, new_occupations):
    """
    """
    for resource in candidate_resources:
        resource_new_occupations = [y[1] for y in filter(lambda x: x[0] == resource, new_occupations)]
        #check availability
        availability = resource.get('availability')
        if availability and not is_datetime_range_available(dt_range, availability):
            continue
        
        #check occupations
        occupations =  resource.get('occupation', []) + resource_new_occupations
        overlappings = [overlaps(dt_range, x) for x in occupations]
        if any(overlappings):
            continue

        return resource
        
    return None



def get_resources_for_dt_range(loop_dt_range, service_recipe, resources):
    """

    """
    new_occupations = []

    for resource_needed in service_recipe:
        candidate_resources = filter(lambda x: x['type'] == resource_needed['type'], resources)
        
        for period in resource_needed['delta_periods']:
            dt_range = by_timedelta_range(period, loop_dt_range[0])
            
            new_occupations_for_type = filter(lambda x: x[0]['type'] == resource_needed['type'], new_occupations)
            available_resource = get_resource_occupation(candidate_resources, dt_range, new_occupations_for_type)
            if available_resource is None:
                return None

            #TODO: check also availability key
            clean_resource  = dissoc(available_resource,'occupations')
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
    * availability: dict describing ....
    * service_recipe: list of needed resources and relative timings
    * resources: availability (from configuration) and occupation (from allocated services) of each resource
    """
    
    ranges = []

    period_start_dt, period_end_dt = period

    delta_duration = get_service_duration(service_recipe)
    delta_step = get_service_step(service_recipe)
    
    loop_dt_range = by_timedelta_range((timedelta(0), delta_duration), period_start_dt)

    while contains(period, loop_dt_range):

        #print "a", loop_dt_range
        if not is_datetime_range_available(loop_dt_range, availability):
            near_working_dt_range = nearest_working_datetime_range(loop_dt_range, availability)
            #print "b", near_working_dt_range
            if near_working_dt_range is not None:
                #print 1
                loop_dt_range = by_timedelta_range((timedelta(0), delta_duration), near_working_dt_range[0])
            else:
                #print 2
                loop_dt_range = by_timedelta_range((timedelta(0), delta_duration), start_of_tomorrow(loop_dt_range[0].date()))

            continue
        

        #TODO: check resources for loop_dt_range
        resources_for_dt_range = get_resources_for_dt_range(loop_dt_range, service_recipe, resources)
        if resources_for_dt_range:
            ranges.append((loop_dt_range, resources_for_dt_range))


        # like i++ but more cool
        loop_dt_range = by_timedelta_range((delta_step, delta_step + delta_duration), loop_dt_range[0])


    return ranges

