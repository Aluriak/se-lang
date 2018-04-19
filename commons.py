"""Globally used definitions"""
import itertools


# Generator of UID
_uid_gen = itertools.count(1)
uid_gen = lambda: next(_uid_gen)



def asp_value_to_pyvalue(value:str or iter or any) -> float or int:
    """

    >>> asp_value_to_pyvalue(2)
    2
    >>> asp_value_to_pyvalue('"3.4"')
    3.4
    >>> asp_value_to_pyvalue(('2', '"3.4"'))
    (2, 3.4)
    >>> asp_value_to_pyvalue(('2', ('"3.4"',))
    (2, (3.4,))

    """
    if isinstance(value, str):
        value = value.strip('"')
        if value.count('.') == 1 and all(part.isnumeric() for part in value.split('.')):
            return float(value)
        elif value.isnumeric():
            return int(value)
    if isinstance(value, (list, tuple)):
        return type(value)(map(asp_value_to_pyvalue, value))
    return value
