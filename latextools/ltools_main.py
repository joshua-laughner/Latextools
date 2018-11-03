import argparse

from .labels import freeze_xrefs


def parse_args():
    parser = argparse.ArgumentParser(description='Suite of tools to automate certain tasks with LaTeX files')

    subparsers = parser.add_subparsers()
    freeze_parser = subparsers.add_parser('freeze-xrefs', help='Convert external references to static text.')
    freeze_xrefs.parse_args(freeze_parser)

    args = vars(parser.parse_args())
    driver_fxn = args.pop('driver_fxn')

    return driver_fxn, args


def main():
    driver, args = parse_args()
    driver(**args)


if __name__ == '__main__':
    main()
