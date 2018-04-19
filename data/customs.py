"""A complex example, showcase for many features"""

from selang import compile_to_se, compile_to_gen, ref, planet, star, orbit, ring


orbits = {
    1: (
        (ring([ref('earth', earth_mass=0.6)] * 7 + [4]), orbit(0.5, eccentricity=0.9)),
        (star('M5V', 0.6), orbit(2, eccentricity=0.7, retrograde=True)),
        (2, orbit(semimajoraxis=1)),
    ),
    2: (3, orbit(0.1)),
    4: (5, orbit(0.005)),
}
objects = {
    1: ref('sun'),
    2: ref('earth'),
    3: ref('moon'),
    4: ref('earth', earth_mass=1.4),
    5: ref('earth', earth_mass=1.2),
}

one, two = compile_to_se('custom system', orbits, objects,
                         '~/games/space_engine/SpaceEngine/', overwrite=True)
print('FILES:', one, two)
