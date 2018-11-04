import argparse

from .labels import freeze_xrefs
from .figures import collect_figures


def parse_args():
    parser = argparse.ArgumentParser(description='Suite of tools to automate certain tasks with LaTeX files')

    subparsers = parser.add_subparsers()
    freeze_parser = subparsers.add_parser('freeze-xrefs', help='Convert external references to static text.')
    freeze_xrefs.parse_args(freeze_parser)

    col_figs_parser = subparsers.add_parser('collect-figs', help='Collect figures into a folder for final publication')
    collect_figures.parse_args(col_figs_parser)

    args = vars(parser.parse_args())
    driver_fxn = args.pop('driver_fxn')

    return driver_fxn, args


def main():
    driver, args = parse_args()
    driver(**args)


if __name__ == '__main__':
    main()
