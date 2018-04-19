"""Routines performing the compilation of input data toward the streams
of SpaceEngine scripts.

"""
import os
import itertools
from pprint import pprint

from . import serepr
from . import commons
from .commons import uid_gen
from .objects import OBJECTS, Orbit, Ring
from .objects_builder import ref


def compile_to_se(system_name:str, orbits:dict or tuple, objects:dict,
                  se_addons_dir:str or (str, str), overwrite:bool=False) -> (str):
    """Return names of written files"""
    star_lines, planet_lines = compile_to_gen(system_name, orbits, objects)
    system_name = system_name.replace(' ', '_')

    # choose the files to write
    if isinstance(se_addons_dir, str):
        star_file = se_addons_dir, 'addons/catalogs/stars/'
        planet_file = se_addons_dir, 'addons/catalogs/planets/'
        star_fname = planet_fname = system_name + '.sc'
    else:
        assert len(se_addons_dir) == 2, se_addons_dir
        star_file, planet_file = se_addons_dir
        star_fname = system_name + '.star.sc'
        planet_fname = system_name + '.planet.sc'
    star_file = os.path.expanduser(os.path.join(*star_file, star_fname))
    planet_file = os.path.expanduser(os.path.join(*planet_file, planet_fname))

    if not overwrite:
        if os.path.exists(star_file):
            raise ValueError("Star record already exists: {}".format(star_file))
        if os.path.exists(planet_file):
            raise ValueError("Planet record already exists: {}".format(star_file))
    with open(star_file, 'w') as fd:
        for line in star_lines:
            fd.write(line + '\n')
    with open(planet_file, 'w') as fd:
        for line in planet_lines:
            fd.write(line + '\n')
    return star_file, planet_file


def compile_to_gen(system_name:str, orbits:dict, objects:dict) -> ([str], [str]):
    """Return two generators of SpaceEngine script lines, one for the star file,
    one for the planet file.

    system_name -- name of the system in SpaceEngine
    orbits -- map from objects to orbiters and orbit info
    objects -- map from object uid to object definition

    """
    orbits = tuple(uniformized_orbits(orbits))
    # print('ORBITS:', orbits)
    orbits, objects, old_uids, uids = uidfy_data(orbits, objects)
    # print('UIDFY:', orbits, objects, old_uids)
    name_of = lambda uid: system_name + '_' + str(type(objects[uid]).__name__).lower() + '_' + str(uid)

    # get root
    roots, inc_tree = make_inclusion_tree(orbits, uids)  # root uid -> {child_uid: {subchild uid: ...}}
    if len(roots) != 1:
        raise ValueError("Invalid number of roots. The {} roots are: {}".format(len(roots), ', '.join(map(str, roots))))
    root = next(iter(roots))
    del roots

    # compute se-repr of root
    star_lines = serepr.of_star_record(system_name)
    planet_lines = serepr.of_root(objects[root], name_of(root), system_name)
    # compute se-repr of each object
    for parent, child, orbit in orbits:
        lines = serepr.of_object(objects[child], name_of(child), name_of(parent),
                                 content=serepr.of_orbit(orbit))
        planet_lines = itertools.chain(planet_lines, lines)
    return star_lines, planet_lines


def make_inclusion_tree(orbits, uids) -> (set, dict):
    direct_inclusions = {}  # parent -> child
    for parent, child, orbit in orbits:
        direct_inclusions.setdefault(parent, set()).add(child)
    # print('DIRECT INCLUSIONS:', direct_inclusions)
    assert not any(parent in childs for parent, childs in direct_inclusions.items())
    def all_childs_of(parent, inclusions=direct_inclusions) -> [object]:
        """Yield all childs of given parent"""
        ret = []
        for child in inclusions.get(parent, ()):
            ret.append(child)
            ret.extend(all_childs_of(child, inclusions))
        return ret
    # close transitivity
    for parent in tuple(direct_inclusions.keys()):
        for child in all_childs_of(parent):
            direct_inclusions[parent].add(child)

    # print('INCLUSIONS:', direct_inclusions)
    roots = set(direct_inclusions.keys()) - set(itertools.chain.from_iterable(direct_inclusions.values()))
    if not roots:
        roots = set(direct_inclusions.keys())
    # print('ROOTS:', roots)
    return roots, direct_inclusions


def uidfy_data(orbits, objects) -> (dict, dict, dict, dict):
    """Return the same data, but with all user defined uid replaced by general uid,
    and all objects pushed into objects pool (no one-time-use objects).

    orbits -- orbit data
    objects -- map object uid -> object definition

    Returns:
    orbits -- orbit data
    objects -- map object uid -> object definition
    old_to_new_uids -- map old uid -> new uid
    user_to_new_uid -- map user uid -> new uid


    """
    new_orbits = []
    new_objects = {}
    old_to_new_uids = {}
    uids = {useruid: uid_gen() for useruid in objects.keys()}  # user uid -> uid

    def make_uid(value):
        """Return an uid associated to given value. If value is not in uids map,
        then it's assumed to be a one-time-use lambda object"""
        already_seen = value in old_to_new_uids
        lambda_object = value not in uids and type(value) in OBJECTS
        raw_object = value not in uids and type(value) not in OBJECTS
        if already_seen:
            # print('EXISTING:', value, ' -> ', old_to_new_uids[value])
            return old_to_new_uids[value]
        if lambda_object:
            new_uid = uid_gen()
            new_objects[new_uid] = value
            # print('LAMBDA:', value, ' -> ', new_uid)
        elif raw_object:  # hope it's in refs
            # print('RAW LAMBDA:', value)
            return make_uid(ref(value))
        else:
            new_uid = uids[value]
            # print('USER DEFINED OBJECT:', value, objects[value], uids[value], new_uid)
            new_objects[new_uid] = objects[value]
            old_to_new_uids[value] = new_uid

        return new_uid

    # print('ORBITS:')
    # pprint(orbits)
    for parent, child, orbit in orbits:
        if isinstance(child, Ring) or isinstance(objects.get(child), Ring):
            child = objects.get(child, child)
            base_orbit = orbit._asdict()
            angle = orbit.angle
            for body, angle_step in zip(child.bodies, child.angle_steps):
                angle = (angle + angle_step) % 360
                base_orbit['angle'] = angle
                orbit = Orbit(**base_orbit)  # orbit specific to the child
                new_orbits.append((make_uid(parent), make_uid(body), orbit))
        else:
            new_orbits.append((make_uid(parent), make_uid(child), orbit))

    return tuple(new_orbits), new_objects, old_to_new_uids, uids


def uniformized_orbits(orbits:dict or tuple) -> [tuple]:
    if isinstance(orbits, dict):
        for parent, childs in orbits.items():
            assert isinstance(childs, (tuple, list))
            if childs and isinstance(childs[0], (tuple, list)):
                assert len(childs[0]) == 2
                yield from ((parent, child, orbit) for child, orbit in childs)
            elif len(childs) == 2:
                yield (parent, *childs)
            else:
                raise ValueError("Unexpected orbit data for parent {}: {}".format(parent, childs))
    else:
        yield from orbits
