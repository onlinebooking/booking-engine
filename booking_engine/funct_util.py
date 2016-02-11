def any_match(predicate, iterable):
    """
    Return True if any element of the iterable match the predicate.
    """
    if predicate is None:
        predicate = bool
    for x in iterable:
        if predicate(x):
            return True
    return False


def first_match(predicate, iterable):
    """
    Return the first element of iterable that match the predicate.
    """
    if predicate is None:
        predicate = bool
    for x in iterable:
        if predicate(x):
            return x
    return None

