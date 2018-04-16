"""Globally used definitions"""
import itertools
from collections import namedtuple


# Model structure
Model = namedtuple('Model', 'system_name, root, root_uid, orbits')
# Orbit structure
Orbit = namedtuple('Orbit', 'parent, orbiter, orbiter_uid, semimajoraxis, eccentricity, inclination, angle, isretrograde')
Orbit.__new__.__defaults__ = 0, 0, 0, False,


# Generator of UID
_uid_gen = itertools.count(1)
uid_gen = lambda: next(_uid_gen)
