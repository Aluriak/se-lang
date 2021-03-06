"""Routines for model manipulation.

"""

import os
from . import asp_model
from . import json_model
from . import commons
from .objects import Model
from .compile import compile_to_gen, compile_to_se, uidfy_data, uniformized_orbits
from .objects_builder import planet, orbit, ring, star, ref


def models_to_se(models:[Model] or Model, se_addons_dir:str or (str, str)):
    """Print given models into their dedicated files, into se addon dir"""
    for model in ([models] if isinstance(models, Model) else models):
        print('SYSTEM: {} ({} orbits)'.format(model.system_name, len(model.orbits)))
        print('FILES:', '\n       '.join(model_to_se(model, se_addons_dir)))
        print()

def model_to_se(model:Model, se_addons_dir:str):
    """Print given model into its dedicated files, into se addon dir"""
    return compile_to_se(model.system_name, model.orbits, model.objects,
                         se_addons_dir, overwrite=True)


def as_model(system_name:str, orbits:dict or tuple, objects:dict) -> Model:
    """Return Model defined by given data by applying
    some uniformization routines on it.

    Do not build a Model without this function, or you will end up with errors
    involving types and attributes mismatches.

    """
    orbits, objects, *_ = uidfy_data(tuple(uniformized_orbits(orbits)), objects)
    return Model(system_name, tuple(orbits), objects)


def get_models(fname:str or iter) -> [Model]:
    """Yield Models from file of given name, either in JSON or ASP"""
    ext_to_class = {
        '.lp': asp_model,
        '.json': json_model,
    }
    ext = os.path.splitext(fname)[1]
    try:
        extractor = ext_to_class[ext]
    except KeyError:
        raise ValueError("Extension {} is not handled".format(ext))
    yield from (model_from(datum, extract=extractor) for datum in extractor.data(fname))


def model_from(raw_data, extract) -> Model:
    """Extract Model from ASP answer sets or JSON data"""
    orbits = list()
    objects = {}

    root_uid, system_name, *other_data = extract.root_info(raw_data, objects)
    assert root_uid in objects

    extract.populate_orbits(raw_data, orbits, objects, root_uid, *other_data)  # side effect

    # from pprint import pprint
    # print()
    # print('ORBITS:')
    # pprint(orbits)
    # print('OBJECTS:')
    # pprint(objects)

    return as_model(str(system_name), orbits, objects)
