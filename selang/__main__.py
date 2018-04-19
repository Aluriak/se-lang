"""CLI entry point for the package.

"""

import os
from . import cli

from . import get_models, models_to_se


if __name__ == '__main__':
    args = cli.parse_args(description=__doc__)
    # print('ARGS:', args)
    if args.se_dir is None:  # user choose a test dir
        outdir = args.test_dir, args.test_dir
    else:  # user gives us a good ol' space engine directory
        outdir = args.se_dir
    models = get_models(args.infile)
    models_to_se(models, outdir)
