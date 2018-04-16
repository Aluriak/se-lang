

SE_STAR = """
Star    "{name}"
{{
    ParentBody "{parent}"
    Class      "{spectral_class}"
    MassSol    {solar_masses}
    RadSol    {solar_radius}
    NoPlanets  {no_procgen}
    AccretionDisk no
""".strip()

SE_PLANET = """
Planet    "{name}"
{{
    ParentBody     "{parent}"
    Class          "{cls}"
    Mass           {earth_masses}
    NoPlanets      {no_procgen}
""".strip()


def se_star(parent:str, name:str, spectral_class:str='G2V', solar_masses:float=1.0, solar_radius:float=1.0, procgen:bool=False, content:[str]=()) -> [str]:
    yield SE_STAR.format(name=name, parent=parent, spectral_class=spectral_class, solar_masses=solar_masses, solar_radius=solar_radius, no_procgen=not procgen)
    if content:
        yield from content
    yield '}'

def se_planet(parent:str, name:str, cls:str='terra', earth_masses:float=1.0, procgen:bool=False, content:[str]=()) -> [str]:
    yield SE_PLANET.format(name=name, parent=parent, cls=cls, earth_masses=earth_masses, no_procgen=not procgen)
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
