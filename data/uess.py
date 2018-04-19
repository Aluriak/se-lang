import itertools
from selang import ref, orbit, ring, model, model_to_se, as_model

def orbits():
    return (
        (str(value / 100), retro, 42, 'earth')
        for value, retro in zip(range(100, 112, 2), itertools.cycle((True, False)))
    )

hierarchy = (
    (1, ring(nb_earth, earth_type), orbit(dist, retrograde=retro))
    for dist, retro, nb_earth, earth_type in orbits()
)
objects = {
    1: 'sun'
}


model = as_model('The Ultimate Engineered Solar System', hierarchy, objects)
model_to_se(model, '~/games/space_engine/SpaceEngine/')
