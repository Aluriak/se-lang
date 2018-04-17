"""Routines to build model from ASP data"""

import clyngor
from commons import Model, Orbit, uid_gen, asp_value_to_pyvalue


ORBIT_ARGS_ORDER = ('semimajoraxis', 'eccentricity', 'obliquity', 'inclination', 'angle')
STAR_ARGS_ORDER = ('spectral_class', 'solar_radius', 'solar_mass')
PLANET_ARGS_ORDER = ('cls', 'earth_radius', 'earth_mass')


def data(fname:str) -> [dict]:
    """Yield the extracted data from given file"""
    yield from clyngor.solve(fname).by_predicate.parse_args.careful_parsing


def root_info(asp_model, objects:dict) -> (str or tuple, str, str, ...):
    roots = tuple(args for args in asp_model.get('root', ()) if len(args) >= 2)
    if len(roots) > 1:
        print('Multiple roots. Bad.')
        exit(1)
    elif len(roots) == 1:
        format_ = lambda x: (str(x).strip('"') if isinstance(x, str) else x)
        args = tuple(map(format_, roots[0]))
        if len(args) == 2:
            root, name = args
            uid = name
        elif len(args) == 3:
            root, name, uid = args
        else:
            raise ValueError("Expect a root/2 or root/3 atom.")
    else:
        print('No root. Bad.')
        exit(1)  # TODO: determine the root by yourself

    types, names = _types_and_names(asp_model, objects)
    return types.get(root, root), name, uid, types, names, root


def populate_orbits(asp_model, orbits:list, objects:dict, root_uid:str,
                    types:dict, names:dict, root_number:int):
    names[root_number] = root_uid
    for args in asp_model.get('orbit', ()):
        orbits.extend(gen_orbits(args, objects, types, names))


def gen_orbits(args:tuple, objects:dict, types:dict, names:dict) -> [Orbit]:
    if len(args) >= 3:
        parent, child, orbit_params, *properties = args

        # Compute orbit parameters
        if isinstance(orbit_params, (str, int)):
            orbit_params_map = {'semimajoraxis': asp_value_to_pyvalue(orbit_params)}
        elif not isinstance(orbit_params, tuple) or len(orbit_params) != 2:
            raise ValueError("Unexpected orbit parameters: {}".format(orbit_params))
        else:  # it's a tuple !
            predicat, orbit_params = orbit_params
            orbit_params_map = {
                k: asp_value_to_pyvalue(v)
                for k, v in dict(zip(ORBIT_ARGS_ORDER, orbit_params)).items()
            }
        distance = orbit_params_map['semimajoraxis']  # shortcut

        # Compute objects representation
        if isinstance(child, tuple) and child[0] in {'planet', 'star'}:
            child, obj = _asp_tuple_to_object(child)
            objects[child] = obj
        if isinstance(parent, tuple) and parent[0] in {'planet', 'star'}:
            parent, obj = _asp_tuple_to_object(parent)
            objects[parent] = obj

        properties = set(properties)
        retrograde = 'retrograde' in map(lambda s: s.strip('"'), properties)
        parent = names.get(parent, parent)
        if isinstance(child, (int, str)):
            try:
                child_type = types.get(child, child)
            except KeyError:
                raise ValueError("Unknow type (is/2) for element of uid {}".format(child))
            child = names.setdefault(child, str(child) + str(uid_gen()))
        # orbit cases
        if isinstance(child, tuple) and child[0] == 'orbit':
            # recursive handling of the childs
            subargs = child[1]
            assert len(subargs) >= 3
            # link between parent and direct child
            yield from gen_orbits((parent, subargs[0], distance), objects, types, names)
            # subsequent links
            yield from gen_orbits(subargs, objects, types, names)
        elif isinstance(child, tuple) and child[0] == 'ring':
            ring_params = child[1]
            if 'angle' in orbit_params_map:
                raise ValueError("Orbit parameters specify an angle, but the object is a ring.")
            assert len(child) == 2 and len(ring_params) >= 2
            ring_type, number, *properties = ring_params
            angle_step = 360 / number
            ring_orbits = []
            for idx in range(number):
                angle = idx * angle_step
                ring_orbits.append(
                    Orbit(names.get(parent, parent), ring_type, ring_type + str(uid_gen()),
                          **orbit_params_map, angle=angle, isretrograde=retrograde)
                )
            for prop in properties:
                if len(prop) == 2 and prop[0] == 'orbit' and len(prop[1]) >= 3:
                    subargs = prop[1]
                    index = subargs[0]
                    if (index-1) in range(len(ring_orbits)):
                        parent = ring_orbits[index].orbiter_uid
                        yield from gen_orbits((parent, *subargs[1:]), objects, types, names)
            yield from ring_orbits
        elif isinstance(child, str):
            yield Orbit(names.get(parent, parent), child_type, child,
                        isretrograde=retrograde, **orbit_params_map)
        else:
            raise ValueError("Non handlable orbit data '{}' (understood as '{}')"
                             "".format(args, (parent, child, distance, properties)))
    else:
        print('Non valid: {}'.format(args))


def _types_and_names(asp_model, objects:dict) -> (dict, dict):
    types = {}  # integer uid -> object types
    names = {}  # integer uid -> object name
    for args in asp_model.get('is', ()):
        if len(args) == 2:
            uid, obj = args
            if uid in types:
                raise ValueError("UID {} given multiple (at least two) times. "
                                 "One for '{}', One for '{}'"
                                 "".format(uid, types[uid], obj))
            if isinstance(obj, tuple):
                obj, obj_repr = _asp_tuple_to_object(obj)
                objects[obj] = obj_repr
            types[uid] = obj
            names[uid] = obj + str(uid_gen())
    return types, names

def _asp_tuple_to_object(atom:tuple) -> (str, dict):
    """Return the unique id and the dict representation of given planet or star object"""
    assert isinstance(atom, tuple) and atom[0] in {'planet', 'star'}
    args_order = PLANET_ARGS_ORDER if atom[0] == 'planet' else STAR_ARGS_ORDER
    new_uid = str(uid_gen())
    data = dict(zip(args_order, atom[1]))
    data['type'] = atom[0]
    return new_uid, data
