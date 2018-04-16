"""
"""
import os
import itertools
from pprint import pprint

from commons import Model, Orbit
from templates import se_star, se_planet, se_orbit
import cli


def get_models(fname:str or iter) -> [Model]:
    """Yield Models from file of given name, either in JSON or ASP"""
    import asp_model, json_model
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


def model_from(asp_model, extract) -> Model:
    """Extract Model from ASP answer sets"""
    orbits = list()

    root, NAME, UID, *other_data = extract.root_info(asp_model)
    root_uid = UID + '__' + NAME
    system_name = root_uid + ' system'

    extract.populate_orbits(asp_model, orbits, root_uid, *other_data)  # side effect

    return Model(str(system_name), root, root_uid, tuple(orbits))


def system_to_se(system_name:str) -> [str]:
    yield 'Remove "' + system_name + '"'
    yield 'StarBarycenter    "' + system_name + '"'
    yield '{}'


def root_to_se(body:tuple or str, name:str, parent:str, content:[str]=()) -> [str]:
    """Return the Space Engine version of given object"""
    if isinstance(body, str):
        yield from name_to_se(body, parent, name, content)
    else:
        raise NotImplementedError


def name_to_se(name:str, parent:str, uid:str, content:[str]) -> [str]:
    if not isinstance(name, str):
        raise TypeError("Can't handle given value of type {} as name: {}".format(type(name), name))
    name = name.replace(' ', '_').lower()
    name = name.lower().replace(' ', '_')
    if name == 'sun':
        yield from se_star(parent=parent, name=uid, content=content)
    elif name == 'red_dwarf':
        yield from se_star(parent=parent, name=uid, content=content, solar_masses=0.1, spectral_class='M5V')
    elif name == 'blue_giant':
        yield from se_star(parent=parent, name=uid, content=content, solar_masses=10, spectral_class='O9')
    elif name == 'earth':
        yield from se_planet(parent=parent, name=uid, content=content)
    elif name == 'moon':
        yield from se_planet(parent=parent, name=uid, content=content, cls='luna', earth_masses=0.1)
    elif name == 'black_hole':
        yield from se_star(parent=parent, name=uid, content=content, spectral_class='X', solar_masses=2000)
    else:
        raise NotImplementedError("Non-implemented name: '{}'".format(uid))


def gen_lines(model:Model) -> ([str], [str]):
    """Return the lines to put into star and planet file"""
    # print the system to put into star catalog
    star_lines = system_to_se(model.system_name)

    # system root
    planet_lines = root_to_se(model.root, name=model.root_uid, parent=model.system_name)

    # show orbits
    # print('MODEL:', model.root)
    # pprint(model.orbits)

    # add the other bodies
    for orbit in model.orbits:
        parent, orbiter, orbiter_uid, semimajoraxis, eccentricity, inclination, angle, isretrograde = orbit
        orbit_params = se_orbit(semimajoraxis, eccentricity, inclination, angle, isretrograde)
        parent = (model.root_uid + '__' + parent) if parent != model.root_uid else parent
        orbiter_uid = (model.root_uid + '__' + orbiter_uid) if orbiter_uid != model.root_uid else orbiter_uid
        planet = name_to_se(orbiter, parent=parent, uid=orbiter_uid, content=orbit_params)
        planet_lines = itertools.chain(planet_lines, planet)

    return star_lines, planet_lines


def write_models(fname:str, star_dir:str, planet_dir:str, rewrite:bool):
    """Write in given dir the files described in file of given name"""
    for model in get_models(fname):
        print('SYSTEM: {} ({} orbits)'.format(model.system_name, len(model.orbits)))
        star_lines, planet_lines = gen_lines(model)
        system_name = model.system_name.title().replace(' ', '_') + '.sc'
        star_file = os.path.join(star_dir, system_name)
        planet_file = os.path.join(planet_dir, system_name)
        print('FILES:', star_file)
        print('      ', planet_file)
        if os.path.exists(star_file) and not rewrite:
            raise RuntimeError("File {} already exists. You may want to use "
                               "--overwrite.".format(star_file))
        if os.path.exists(planet_file) and not rewrite:
            raise RuntimeError("File {} already exists. You may want to use "
                               "--overwrite.".format(planet_file))
        with open(star_file, 'w') as fd:
            for line in star_lines:
                fd.write(line + '\n')
        with open(planet_file, 'w') as fd:
            for line in planet_lines:
                fd.write(line + '\n')
        print()


if __name__ == '__main__':
    args = cli.parse_args(description=__doc__)
    # print('ARGS:', args)
    if args.se_dir is None:  # user choose a test dir
        star_dir, planet_dir = args.test_dir, args.test_dir
    else:  # user gives us a good ol' space engine directory
        star_dir = os.path.join(args.se_dir, 'addons/catalogs/stars/')
        planet_dir = os.path.join(args.se_dir, 'addons/catalogs/planets/')
    write_models(args.infile, star_dir, planet_dir, args.overwrite)
