"""Definitions for general objects"""


from collections import namedtuple
from . import templates


ORBIT_ARGS_ORDER = ('semimajoraxis', 'eccentricity', 'obliquity', 'inclination',
                    'ascending_node', 'arg_of_pericenter', 'angle',
                    'refplane', 'retrograde')
STAR_ARGS_ORDER = ('spectral_class', 'solar_mass', 'solar_radius')
PLANET_ARGS_ORDER = ('cls', 'earth_mass', 'earth_radius')
RING_ARGS_ORDER = ('nb_body', 'bodies', 'angle_steps')
BARY_ARGS_ORDER = ()


# Model structure
Model = namedtuple('Model', 'system_name, orbits, objects')
# Astres structures
Star = namedtuple('Star', STAR_ARGS_ORDER)
Planet = namedtuple('Planet', PLANET_ARGS_ORDER)
Ring = namedtuple('Ring', RING_ARGS_ORDER)
Barycenter = namedtuple('Barycenter', BARY_ARGS_ORDER)
# Orbit structures
Orbit = namedtuple('Orbit', ORBIT_ARGS_ORDER)
Orbit.__new__.__defaults__ = 0, 0, 0, None, None, 0, 'Equator', False


OBJECTS = {Barycenter, Star, Planet, Ring}
OBJECTS_NAME = {obj.__name__.lower() for obj in OBJECTS}


def se_repr(template:callable, framed=True):
    if framed:
        def se_repr_gen(obj:object, name:str, parent:str, content:[str]=()) -> [str]:
            yield from template(parent, name, *obj, content=content)
    else:
        def se_repr_gen(obj:object) -> [str]:
            yield from template(*obj)
    return se_repr_gen
Orbit.se_repr = se_repr(templates.se_orbit, framed=False)
Planet.se_repr = se_repr(templates.se_planet)
Star.se_repr = se_repr(templates.se_star)
Barycenter.se_repr = se_repr(templates.se_barycenter)
