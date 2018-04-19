"""Templating of SpaceEngine script for various objects.

"""
from . import templates


def of_star_record(system_name:str) -> [str]:
    yield 'Remove "' + system_name + '"'
    yield 'StarBarycenter    "' + system_name + '"'
    yield '{}'

def of_root(root:object, name:str, system_name:str):
    """SpaceEngine script representation of the root."""
    return root.se_repr(name, system_name)

def of_object(obj:object, name:str, parent:str, *, content:[str]=()):
    """SpaceEngine script representation of given star or planet."""
    return obj.se_repr(name, parent, content=content)

def of_orbit(orbit:object):
    """SpaceEngine script representation of given Orbit."""
    return orbit.se_repr()
