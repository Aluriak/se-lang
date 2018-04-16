"""Definition of the CLI.
"""

import os
import argparse


def parse_args(description:str, args:iter=None) -> dict:
    return cli_parser(description).parse_args(args)

def existant_file(filepath:str) -> str:
    """Argparse type, raising an error if given file does not exists"""
    if not os.path.exists(filepath):
        raise argparse.ArgumentTypeError("file {} doesn't exists".format(filepath))
    return filepath

def existant_dir(filepath:str) -> str:
    """Argparse type, raising an error if given file does not exists"""
    if not os.path.isdir(filepath):
        raise argparse.ArgumentTypeError("directory {} doesn't exists".format(filepath))
    return filepath

def se_dir(filepath:str) -> str:
    """Argparse type, raising an error if given directory is not a SpaceEngine directory"""
    existant_dir(filepath)
    dirs = set()
    expected_dirs = {'addons', 'config', 'system'}
    dirs = {entry.name for entry in os.scandir(filepath) if entry.is_dir()}
    not_found = expected_dirs - dirs
    if not_found:
        raise argparse.ArgumentTypeError("SpaceEngine directory {} doesn't "
                                         "contains expected subdir: {}"
                                         "".format(filepath, ', '.join(no_found)))
    return filepath

def writable_file(filepath:str) -> str:
    """Argparse type, raising an error if given file is not writable.
    Will delete the file !
    """
    try:
        with open(filepath, 'w') as fd:
            pass
        os.remove(filepath)
        return filepath
    except (PermissionError, IOError):
        raise argparse.ArgumentTypeError("file {} is not writable.".format(filepath))


def cli_parser(description:str) -> argparse.ArgumentParser:
    # main parser
    parser = argparse.ArgumentParser(description=description.strip())

    parser.add_argument('infile', type=existant_file,
                        help="Name of the input file containing the system to render")

    # user may want to put automatically the system in place, or anywhere without treatment
    outdir = parser.add_mutually_exclusive_group()
    outdir.add_argument('--se-dir', '-o', type=se_dir,
                        help="Where SpaceEngine is installed")
    outdir.add_argument('--test-dir', '-t', type=existant_dir, default='.',
                        help="Where to put the files")

    parser.add_argument('--overwrite', action='store_true',
                        help="Rewrite existing files")

    return parser
