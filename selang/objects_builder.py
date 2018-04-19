"""Routines to build the objects."""

import inspect
from itertools import islice, cycle
from .objects import Planet, Orbit, Ring, Star, OBJECTS


orbit = Orbit


def ring(nb_body:int=None, bodies:object=None, *, angle_steps:float or iter=None) -> Ring:
    """Define a ring object.

    bodies -- either one object, or an iterable of objects
    nb_body -- number of body to put in the ring.

    If bodies is an iterable and nb_body is given, the ring will contains
    the nb_body firsts items of the iterable.

    """
    # invert arguments if any mixing
    if nb_body and not bodies and not isinstance(nb_body, int):
        bodies, nb_body = nb_body, None
    # compute bodies
    if inspect.isgenerator(bodies) or isinstance(bodies, (list, tuple)):
        if nb_body is None:
            bodies = tuple(bodies)
        else:  # take the given number in given iterable
            bodies = tuple(islice(cycle([bodies]), 0, int(nb_body)))
    else:
        bodies = (bodies,) * int(nb_body)
    nb_body = len(bodies)
    # compute angle steps
    if angle_steps is None:  # make them evenly distributed
        angle_steps = [360 / nb_body] * nb_body
    elif isinstance(angle_steps, (int, float)):
        angle_steps = [angle_steps] * nb_body
    else:
        angle_steps = tuple(islice(cycle(angle_steps), 0, nb_body))
    return Ring(
        nb_body=len(bodies),
        bodies=bodies,
        angle_steps=tuple(angle_steps),
    )


def star(spectral_class:str, solar_radius:float=None, solar_mass:float=None) -> Star:
    return Star(
        str(spectral_class),
        *_astre_mass_radius(solar_mass, solar_radius),
    )

def planet(cls:str, earth_radius:float=None, earth_mass:float=None) -> Planet:
    return Planet(
        str(cls),
        *_astre_mass_radius(earth_mass, earth_radius),
    )


def _astre_mass_radius(mass:float=None, radius:float=None) -> (float, float):
    if mass and radius is None:
        radius = mass
    elif radius and mass is None:
        mass = radius
    elif mass and radius:
        pass  # nothing to do
    else:
        raise ValueError("Astre definition: radius or mass must be given (received: {}, {}).".format(mass, radius))
    return float(mass), float(radius)


def ref(name:str, **kwargs) -> star or planet:
    if not isinstance(name, str):
        raise TypeError("Can't handle given value of type {} as name: {}".format(type(name), name))
    name = name.replace(' ', '_').lower()
    if name == 'sun':
        payload = star, {'solar_mass': 1, 'solar_radius': 1, 'spectral_class': 'G2V'}
    elif name == 'red_dwarf':
        payload = star, {'solar_mass': 0.1, 'spectral_class': 'M5V'}
    elif name == 'blue_giant':
        payload = star, {'solar_mass': 10, 'spectral_class': 'O9'}
    elif name == 'earth':
        payload = planet, {'cls': 'terra', 'earth_mass': 1, 'earth_radius': 1}
    elif name == 'moon':
        payload = planet, {'cls': 'luna', 'earth_mass': 0.1}
    elif name == 'black_hole':
        payload = star, {'spectral_class': 'X', 'solar_mass': 2000}
    else:
        raise NotImplementedError("Non-implemented name: '{}'".format(name))
    func, fixed_kwargs = payload
    return func(**{**fixed_kwargs, **kwargs})
