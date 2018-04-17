



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
        yield '    AccretionDisk no'
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
        yield '    Radius         {}'.format(float(earth_radius) * 6378)
    if not procgen:
        yield '    NoPlanets  true'
    if content:
        yield from content
    yield '}'


SE_ORBIT = """
    Obliquity       {obliquity}
    Orbit
    {{
        RefPlane        "Equator"
        SemiMajorAxis   {semimajoraxis}
        Eccentricity    {eccentricity}
        Inclination     {inclination}
        MeanAnomaly     {angle}
        AscendingNode   0
    }}
""".strip('\n')


def se_orbit(semimajoraxis:float, eccentricity:float=0, inclination:float=0, angle:float=0, retrograde:bool=False, obliquity:float=0) -> [str]:
    yield SE_ORBIT.format(semimajoraxis=semimajoraxis, eccentricity=eccentricity,
                          inclination=inclination + (180 if retrograde else 0),
                          angle=angle, obliquity=obliquity)
