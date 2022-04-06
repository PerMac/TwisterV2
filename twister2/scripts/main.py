import argparse

from twister2.scripts.hardware_map import scan


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--generate-hardware-map',
        dest='hardware_map_path',
        metavar='path',
        help='generate hardware map',
    )
    parser.add_argument(
        '--list-hardware-map',
        dest='list_hardware_map',
        action='store_true',
        help='list hardware map',
    )

    args = parser.parse_args()

    if args.hardware_map_path:
        return scan(filename=args.hardware_map_path, persistent=False)
    if args.list_hardware_map:
        return scan(persistent=False)

    parser.print_help()
    return 1
