def functional_setattr(__obj, __name, __value):
    """
    Same as builting setattr but returns __obj instead of None.
    """
    setattr(__obj, __name, __value)
    return __obj
