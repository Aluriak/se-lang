"""Routines to build model from JSON data"""

import json
from commons import Model, Orbit, uid_gen


def data(fname:str) -> [dict]:
    """Yield the extracted data from given file"""
    with open(fname) as fd:
        data = json.load(fd)
        if isinstance(data, list):
            yield from (datum for datum in data if isinstance(datum, dict))
        else:
            assert isinstance(data, dict)
            yield data


def root_info(json_data:dict) -> (str or tuple, str, str):
    return json_data['type'], json_data['name'], json_data.get('UID', json_data['name'])


def populate_orbits(json_data:dict, orbits:list, root_uid:str):
    assert isinstance(json_data, dict), json_data
    if 'childs' in json_data or 'child' in json_data:
        iter_childs = json_data.get('childs', json_data.get('child'))
        if isinstance(iter_childs, dict): iter_childs = [iter_childs]
        for child in iter_childs:
            new_orbits = list(gen_orbits(root_uid, child))
            for subchild in child.get('childs', ()):
                new_orbits += gen_orbits(child['UID'], subchild)
            if 'child' in child:
                new_orbits += gen_orbits(child['UID'], child['child'])
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
                    parent_uid = new_orbits[int(parent_index)].orbiter_uid
                    for subchild in childs:
                        new_orbits += gen_orbits(parent_uid, subchild)

            orbits.extend(new_orbits)


def gen_orbits(parent:str, child:dict) -> [Orbit]:
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
            yield Orbit(parent, ring_type, new_uid, distance, angle=angle, isretrograde=retrograde)
    elif isinstance(child_type, str):
        new_uid = child_type + str(uid_gen())
        child['UID'] = new_uid
        yield Orbit(parent, child_type, new_uid, distance, isretrograde=retrograde)
