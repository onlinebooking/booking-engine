def omit(t, *keys):
    """
    Omit keys from dict, return dict without keys.
    """
    return {key: t[key] for key in t if key not in keys}
