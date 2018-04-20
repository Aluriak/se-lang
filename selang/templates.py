"""Functions bridging internal data and SpaceEngine representation.

"""

def se_star(parent:str, name:str, spectral_class:str=None, solar_masses:float=None, solar_radius:float=None, procgen:bool=False, content:[str]=(), accretion_disk:bool=False) -> [str]:
    yield 'Star    "{}"'.format(name)
    yield '{'
    yield '    ParentBody "{}"'.format(parent)
    if spectral_class:
        yield '    Class      "{}"'.format(spectral_class)
    if solar_masses:
        yield '    MassSol    {}'.format(solar_masses)
    if solar_radius:
        yield '    RadSol    {}'.format(solar_radius)
    if not procgen:
        yield '    NoPlanets  true'
    if not accretion_disk:
        yield '    NoAccretionDisk true'
    if content:
        yield from content
    yield '}'


def se_barycenter(parent:str, name:str, procgen:bool=False, content:[str]=()) -> [str]:
    yield 'StarBarycenter    "{}"'.format(name)
    yield '{'
    yield '    ParentBody     "{}"'.format(parent)
    if not procgen:
        yield '    NoPlanets true'
    if content:
        yield from content
    yield '}'


def se_planet(parent:str, name:str, cls:str=None, earth_masses:float=None, earth_radius:float=None, procgen:bool=False, content:[str]=()) -> [str]:
    yield 'Planet    "{}"'.format(name)
    yield '{'
    yield '    ParentBody     "{}"'.format(parent)
    if cls:
        yield '    Class          "{}"'.format(cls)
    if earth_masses:
        yield '    Mass           {}'.format(earth_masses)
    if earth_radius:
        yield '    Radius         {}'.format(round(float(earth_radius) * 6378, 2))
    if not procgen:
        yield '    NoPlanets  true'
    if content:
        yield from content
    yield '}'


def se_orbit(semimajoraxis:float, eccentricity:float=None, obliquity:float=None, inclination:float=None,
             ascending_node:float=None, arg_of_pericenter:float=None, angle:float=None, refplane:str='equator', retrograde:bool=False) -> [str]:
    if eccentricity is not None:
        yield '    Obliquity       {}'.format(obliquity)
    yield '    Orbit'
    yield '    {'
    yield '        RefPlane        "{}"'.format(refplane)
    yield '        SemiMajorAxis   {}'.format(semimajoraxis)
    if eccentricity is not None:
        yield '        Eccentricity    {}'.format(eccentricity)
    if inclination is not None:
        yield '        Inclination     {}'.format(inclination + (180 if retrograde else 0))
    if angle is not None:
        yield '        MeanAnomaly     {}'.format(angle)
    if ascending_node is not None:
        yield '        AscendingNode   {}'.format(ascending_node)
    if arg_of_pericenter is not None:
        yield '        ArgOfPericenter {}'.format(arg_of_pericenter)
    yield '    }'
