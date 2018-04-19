"""Definitions for general objects"""


import templates
from collections import namedtuple


ORBIT_INFO_ARGS_ORDER = ('semimajoraxis', 'eccentricity', 'obliquity',
                         'inclination', 'angle', 'retrograde')
STAR_ARGS_ORDER = ('spectral_class', 'solar_mass', 'solar_radius')
PLANET_ARGS_ORDER = ('cls', 'earth_mass', 'earth_radius')
RING_ARGS_ORDER = ('nb_body', 'bodies', 'angle_steps')


# Model structure
Model = namedtuple('Model', 'system_name, orbits, objects')
# Astres structures
Star = namedtuple('Star', STAR_ARGS_ORDER)
Planet = namedtuple('Planet', PLANET_ARGS_ORDER)
Ring = namedtuple('Ring', RING_ARGS_ORDER)
# Orbit structures
OrbitInfo = namedtuple('OrbitInfo', ORBIT_INFO_ARGS_ORDER)
OrbitInfo.__new__.__defaults__ = 0, 0, 0, 0, False
Orbit = namedtuple('Orbit', 'parent, child, info')

OBJECTS = {Star, Planet, Ring, OrbitInfo}


def _Orbit__from_params(parent, orbiter, orbiter_uid, semimajoraxis,
                        eccentricity, inclination, angle, retrograde:bool):
    return Orbit(
        parent, orbiter, orbiter_uid,
        OrbitInfo(semimajoraxis, eccentricity, inclination, angle, retrograde)
    )
Orbit.from_params = _Orbit__from_params



def se_repr(template:callable, framed=True):
    if framed:
        def se_repr_gen(obj:object, name:str, parent:str, content:[str]=()) -> [str]:
            yield from template(parent, name, *obj, content=content)
    else:
        def se_repr_gen(obj:object) -> [str]:
            yield from template(*obj)
    return se_repr_gen
OrbitInfo.se_repr = se_repr(templates.se_orbit, framed=False)
Planet.se_repr = se_repr(templates.se_planet)
Star.se_repr = se_repr(templates.se_star)
