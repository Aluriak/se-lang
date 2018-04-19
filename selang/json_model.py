"""Routines to build model from JSON data"""

import json
from .objects import Model, Orbit
from .objects_builder import ref
from .commons import uid_gen


def data(fname:str) -> [dict]:
    """Yield the extracted data from given file"""
    with open(fname) as fd:
        data = json.load(fd)
        if isinstance(data, list):
            yield from (datum for datum in data if isinstance(datum, dict))
        else:
            assert isinstance(data, dict)
            yield data


def root_info(json_data:dict, objects:dict) -> (str, str):
    """Return the root uid and the system name.

    json_data -- json dict containing data
    objects -- dict. Modified, so root_uid maps to the root definition.

    """
    root_type, NAME, UID = json_data['type'], json_data['name'], json_data.get('UID', json_data['name'])
    root_uid = UID + '__' + NAME
    system_name = root_uid + ' system'
    objects[root_uid] = ref(root_type)
    return root_uid, system_name


def populate_orbits(json_data:dict, orbits:list, objects:dict, root_uid:str):
    assert isinstance(json_data, dict), json_data
    if 'childs' in json_data or 'child' in json_data:
        iter_childs = json_data.get('childs', json_data.get('child'))
        if isinstance(iter_childs, dict): iter_childs = [iter_childs]
        for child in iter_childs:
            new_orbits = list(gen_orbits(root_uid, child, objects))
            for subchild in child.get('childs', ()):
                new_orbits += gen_orbits(child['UID'], subchild, objects)
            if 'child' in child:
                new_orbits += gen_orbits(child['UID'], child['child'], objects)
            # handle childs of specific stars of rings
            if 'childof' in child and isinstance(child['childof'], dict):
                for parent_index, childs in child['childof'].items():
                    if isinstance(childs, dict):  # one child
                        childs = [childs]
                    elif isinstance(childs, list):  # list of child
                        pass
                    else:
                        raise ValueError("Unhandlable json value for ring child: {}".format(childs))
                    if not parent_index.isnumeric():
                        raise ValueError("Parent index for childs of rings element must be a integer value, not '{}'".format(parent_index))
                    parent_uid = new_orbits[int(parent_index)][1]
                    for subchild in childs:
                        new_orbits += gen_orbits(parent_uid, subchild, objects)

            orbits.extend(new_orbits)


def gen_orbits(parent:str, child:dict, objects:dict) -> [Orbit]:
    retrograde = child.get('retrograde', False)
    child_type = child.get('type')
    distance = child['distance']
    if isinstance(child_type, (list, tuple)) and child_type[0] == 'ring':
        ring_params = child_type[1:]
        assert len(child_type) >= 2 and len(ring_params) == 2
        number, ring_type = ring_params
        angle_step = 360 / number
        for idx in range(number):
            angle = idx * angle_step
            new_uid = ring_type + str(uid_gen())
            child['UID'] = new_uid
            objects[new_uid] = ref(ring_type)
            yield parent, new_uid, Orbit(distance, angle=angle, retrograde=retrograde)
    elif isinstance(child_type, str):
        new_uid = child_type + str(uid_gen())
        child['UID'] = new_uid
        objects[new_uid] = ref(child_type)
        yield parent, new_uid, Orbit(distance, retrograde=retrograde)
